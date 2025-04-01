import torch
from torch import optim, nn
import torch.nn.functional as F
import lightning.pytorch as pl
from bio_attention.attention import TransformerEncoder
from bio_attention.embed import DiscreteEmbedding, ContinuousEmbedding
from bento_sc import loss
from bento_sc.utils.metrics import pearson_batch_masked
from scipy.stats import pearsonr
from torchmetrics.classification import MulticlassAccuracy
import numpy as np
from copy import deepcopy


class EmbeddingGater(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.embedding = nn.Parameter(torch.empty(dim).uniform_(-1, 1))

    def forward(self, x):
        y = F.tanh(x) * self.embedding
        y[:, 0, :] = x[:, 0, :]
        return y


class EmbeddingPseudoQuantizer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.embedding = nn.Parameter(torch.empty(in_dim, out_dim).uniform_(-1, 1))

    def forward(self, x):
        y = F.softmax(x, dim=-1) @ self.embedding
        y[:, 0, :] = x[:, 0, :]
        return y


class BentoTransformer(pl.LightningModule):
    def __init__(self, config):
        super().__init__()
        self.save_hyperparameters()

        self.config = deepcopy(config)

        if self.config.discrete_input:
            self.embedder = DiscreteEmbedding(
                self.config.n_discrete_tokens, self.config.dim, cls=True
            )
        else:
            self.embedder = ContinuousEmbedding(self.config.dim, cls=True)

        if self.config.pseudoquant_input:
            self.embedder = nn.Sequential(
                self.embedder,
                EmbeddingPseudoQuantizer(self.config.dim, self.config.dim),
            )
        elif self.config.gate_input:
            self.embedder = nn.Sequential(
                self.embedder, EmbeddingGater(self.config.dim)
            )

        self.transformer = TransformerEncoder(
            depth=self.config.depth,
            dim=self.config.dim,
            nh=8,
            attentiontype="vanilla",
            attention_args={
                "dropout": self.config.dropout,
                "enable_math": False,
                "enable_flash": True,
                "enable_mem_efficient": True,
            },
            plugintype="learned",
            plugin_args={"dim": self.config.dim, "max_seq_len": self.config.n_genes},
            only_apply_plugin_at_first=True,
            dropout=self.config.dropout,
            glu_ff=True,
            activation="gelu",
        )

        loss_mapper = {
            "BinCE": loss.BinCE,
            "CountMSE": loss.CountMSE,
            "PoissonNLL": loss.PoissonNLL,
            "NegativeBinomialNLL": loss.NegativeBinomialNLL,
            "ZeroInflatedNegativeBinomialNLL": loss.ZeroInflatedNegativeBinomialNLL,
        }

        loss_type = self.config.loss["type"]
        loss_kwargs = {k: v for k, v in self.config.loss.items() if k != "type"}
        self.loss = loss_mapper[loss_type](self.config.dim, **loss_kwargs)

        if self.config.nce_loss:
            self.nce_loss = loss.NCELoss(
                self.config.dim, self.config.nce_dim, temperature=self.config.nce_temp
            )

        if self.config.celltype_clf_loss:
            self.ct_clf_loss = loss.CellTypeClfLoss(self.config.dim, 164)

        self.lr = float(self.config.lr)

    def forward(self, batch):
        mask = batch["gene_counts"] != -1
        if torch.all(mask):
            mask = None
        x = self.embedder(batch["gene_counts"])
        z = self.transformer(x, pos=batch["gene_index"], mask=mask)
        return z

    def training_step(self, batch, batch_idx):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        if not self.config.train_on_all:
            train_on = torch.isnan(batch["gene_counts"])
        else:
            train_on = None

        y = self(batch)

        if ("no_genewise_loss" in self.config) and (
            self.config["no_genewise_loss"] == True
        ):
            loss = 0
        else:
            loss = self.loss(
                y[:, 1:],
                batch["gene_counts_true"],
                gene_ids=batch["gene_index"],
                train_on=train_on,
            )

        if self.config.nce_loss:
            nce_loss = self.nce_loss(y[:, 0])
            loss += nce_loss

        if self.config.celltype_clf_loss:
            ct_loss = self.ct_clf_loss(y[:, 0], batch["0/obs"][:, 3])
            loss += ct_loss

        self.log("train_loss", loss, sync_dist=True)
        return loss

    def validation_step(self, batch, batch_idx):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        if not self.config.train_on_all:
            train_on = torch.isnan(batch["gene_counts"])
        else:
            train_on = None

        y = self(batch)

        if ("no_genewise_loss" in self.config) and (
            self.config["no_genewise_loss"] == True
        ):
            loss = 0
        else:
            loss = self.loss(
                y[:, 1:],
                batch["gene_counts_true"],
                gene_ids=batch["gene_index"],
                train_on=train_on,
            )

        if self.config.nce_loss:
            nce_loss = self.nce_loss(y[:, 0])
            loss += nce_loss

        if self.config.celltype_clf_loss:
            ct_loss = self.ct_clf_loss(y[:, 0], batch["0/obs"][:, 3])
            loss += ct_loss

        self.log("val_loss", loss, sync_dist=True)

    def predict_step(self, batch):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        y = self(batch)
        libsizes = (batch["gene_counts"].sum(1) + (batch["gene_counts"] == -1).sum(1))[
            :, None
        ]

        count_predictions = self.loss.predict(
            y[:, 1:],
            gene_ids=batch["gene_index"],
            libsize=libsizes,
        )
        if isinstance(count_predictions, tuple):
            count_predictions = count_predictions[0]

        return (batch["0/obs"], y[:, 0], count_predictions, batch["gene_counts_true"])

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.lr)

        return optimizer

    @property
    def config_used(self):
        return {
            "n_discrete_tokens",
            "dim",
            "pseudoquant_input",
            "gate_input",
            "depth",
            "dropout",
            "n_genes",
            "loss",
            "nce_loss",
            "nce_dim",
            "nce_temp",
            "celltype_clf_loss",
            "lr",
            "train_on_all",
        }

    @property
    def config_unused(self):
        return set(self.config) - self.config_used


class PerturbTransformer(BentoTransformer):
    def __init__(self, config):
        super().__init__(config)
        assert self.config.nce_loss == False
        assert self.config.celltype_clf_loss == False
        assert self.config.train_on_all == True
        assert isinstance(self.loss, loss.CountMSE)

        self.perturbation_indicator = nn.Parameter(
            torch.empty(self.config.dim).uniform_(-1, 1)
            / self.config.perturb_init_factor
        )
        self.validation_step_outputs = []

    def forward(self, batch):
        mask = batch["gene_counts"] != -1
        if torch.all(mask):
            mask = None

        x = self.embedder(batch["gene_counts"])

        matches = torch.where((batch["gene_index"].T == batch["0/perturbed_gene"]).T)
        assert (matches[0] == torch.arange(len(x)).to(matches[0].device)).all()
        x[torch.arange(len(x)), matches[1]] += self.perturbation_indicator

        z = self.transformer(x, pos=batch["gene_index"], mask=mask)
        return z

    def training_step(self, batch, batch_idx):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        y = self(batch)

        loss = self.loss(
            y[:, 1:],
            batch["gene_counts_true"].to(y.dtype),
            gene_ids=batch["gene_index"],
        )

        self.log("train_loss", loss, sync_dist=True)
        return loss

    def validation_step(self, batch, batch_idx):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        y = self(batch)

        loss = self.loss(
            y[:, 1:],
            batch["gene_counts_true"].to(y.dtype),
            gene_ids=batch["gene_index"],
        )

        self.log("val_loss", loss, sync_dist=True)

        libsizes = batch["gene_counts_true"].sum(1) + (
            batch["gene_counts_true"] == -1
        ).sum(1)

        y = self.loss.predict(y[:, 1:], libsize=libsizes)

        self.validation_step_outputs.append(
            (
                y.cpu(),
                batch["gene_counts_true"].cpu(),
                batch["gene_counts_copy"].cpu(),
                batch["0/perturbed_gene"].cpu(),
            )
        )

    def on_validation_epoch_end(self):
        pred_pert_prof = torch.cat([s[0] for s in self.validation_step_outputs])
        true_pert_prof = torch.cat([s[1] for s in self.validation_step_outputs])
        perturbed_genes = torch.cat([s[3] for s in self.validation_step_outputs])

        mean_ctrl_profile = torch.cat(
            [s[2] for s in self.validation_step_outputs]
        ).mean(0)

        pearsons = []
        delta_pearsons = []
        for pert_gene in torch.unique(perturbed_genes):
            pred_per_pert = pred_pert_prof[perturbed_genes == pert_gene].float().mean(0)
            true_per_pert = true_pert_prof[perturbed_genes == pert_gene].float().mean(0)

            pred_delta_per_pert = pred_per_pert - mean_ctrl_profile
            true_delta_per_pert = true_per_pert - mean_ctrl_profile

            s1 = pearsonr(pred_per_pert.numpy(), true_per_pert.numpy()).statistic
            pearsons.append(s1)

            s2 = pearsonr(
                pred_delta_per_pert.numpy(), true_delta_per_pert.numpy()
            ).statistic
            delta_pearsons.append(s2)
        self.log("val_pearson", np.mean(pearsons), sync_dist=True)
        self.log("val_deltapearson", np.mean(delta_pearsons), sync_dist=True)

        self.validation_step_outputs.clear()

    def predict_step(self, batch, batch_idx):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        y = self(batch)

        libsizes = batch["gene_counts_true"].sum(1) + (
            batch["gene_counts_true"] == -1
        ).sum(1)
        y = self.loss.predict(y[:, 1:], libsize=libsizes)
        return (
            y,
            batch["gene_counts_true"],
            batch["gene_counts_copy"],
            batch["gene_index"],
        )

    @property
    def config_used(self):
        return {
            "n_discrete_tokens",
            "dim",
            "pseudoquant_input",
            "gate_input",
            "depth",
            "dropout",
            "n_genes",
            "loss",
            "lr",
        }


class CLSTaskTransformer(BentoTransformer):
    def __init__(self, config):
        super().__init__(config)
        assert self.config.nce_loss == False

        if self.config.celltype_clf_loss:
            self.loss = loss.CellTypeClfLoss(
                self.config.dim, self.config.cls_finetune_dim
            )
        elif self.config.modality_prediction_loss:
            self.loss = loss.ModalityPredictionLoss(
                self.config.dim, self.config.cls_finetune_dim
            )
        else:
            raise ValueError(
                "At least one of celltype clf loss or modality predict loss should be true"
            )

        self.validation_step_outputs = []

        if self.config.celltype_clf_loss:
            self.micro_acc = MulticlassAccuracy(
                num_classes=self.config.cls_finetune_dim, average="micro"
            )
            self.macro_acc = MulticlassAccuracy(
                num_classes=self.config.cls_finetune_dim, average="macro"
            )

    def forward(self, batch):
        mask = batch["gene_counts"] != -1
        if torch.all(mask):
            mask = None
        x = self.embedder(batch["gene_counts"])
        z = self.transformer(x, pos=batch["gene_index"], mask=mask)
        return self.loss.predict(z[:, 0])

    def training_step(self, batch, batch_idx):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        y = self(batch)

        loss = self.loss.loss(y, batch["0/targets"])

        self.log("train_loss", loss, sync_dist=True)
        return loss

    def validation_step(self, batch, batch_idx):
        if not self.config.discrete_input:
            batch["gene_counts"] = batch["gene_counts"].to(self.dtype)
        else:
            batch["gene_counts"] = batch["gene_counts"].float()

        y = self(batch)

        loss = self.loss.loss(y, batch["0/targets"])

        self.log("val_loss", loss, sync_dist=True)
        if self.config.celltype_clf_loss:
            self.micro_acc(y, batch["0/targets"])
            self.macro_acc(y, batch["0/targets"])
            self.log(
                "val_microacc",
                self.micro_acc,
                on_step=False,
                on_epoch=True,
                batch_size=len(batch["0/targets"]),
                sync_dist=True,
            )
            self.log(
                "val_macroacc",
                self.macro_acc,
                on_step=False,
                on_epoch=True,
                batch_size=len(batch["0/targets"]),
                sync_dist=True,
            )

        self.validation_step_outputs.append((y.cpu(), batch["0/targets"].cpu()))

    def on_validation_epoch_end(self):
        all_preds = torch.cat([s[0] for s in self.validation_step_outputs])
        all_trues = torch.cat([s[1] for s in self.validation_step_outputs])

        if isinstance(self.loss, loss.ModalityPredictionLoss):
            pearson_per_target = pearson_batch_masked(
                all_preds.T.float(), all_trues.T.float()
            ).numpy()
            self.log("val_macro_pearson", np.mean(pearson_per_target), sync_dist=True)

        self.validation_step_outputs.clear()

    @property
    def config_used(self):
        return {
            "n_discrete_tokens",
            "dim",
            "pseudoquant_input",
            "gate_input",
            "depth",
            "dropout",
            "n_genes",
            "lr",
            "celltype_clf_loss",
            "modality_prediction_loss",
            "cls_finetune_dim",
        }
