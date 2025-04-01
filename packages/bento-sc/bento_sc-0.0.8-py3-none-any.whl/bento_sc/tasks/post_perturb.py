from bento_sc.data import BentoDataModule
from bento_sc.models import PerturbTransformer, BentoTransformer
from bento_sc.utils.config import Config
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping
from lightning.pytorch.loggers import TensorBoardLogger
from lightning.pytorch.plugins.environments import LightningEnvironment
from lightning.pytorch import Trainer
import argparse


def boolean(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def main():
    class CustomFormatter(
        argparse.ArgumentDefaultsHelpFormatter, argparse.MetavarTypeHelpFormatter
    ):
        pass

    parser = argparse.ArgumentParser(
        description="Fine-tuning script for post-perturbation expression prediction evaluation.",
        formatter_class=CustomFormatter,
    )

    parser.add_argument(
        "config_path", type=str, metavar="config_path", help="config_path"
    )
    parser.add_argument(
        "checkpoint", type=str, metavar="checkpoint", help="checkpoint path"
    )
    parser.add_argument("logs_path", type=str, metavar="logs_path", help="logs_path")
    parser.add_argument(
        "--data_path",
        type=str,
        default=None,
        help="Data file. Overrides value in config file if specified",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=None,
        help="Learning rate. Overrides value in config file if specified",
    )
    parser.add_argument(
        "--init_factor",
        type=float,
        default=None,
        help="init_factor. Overrides value in config file if specified",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=None,
        help="Batch size. Overrides value in config file if specified",
    )
    parser.add_argument(
        "--tune_mode",
        type=boolean,
        default=False,
        help="Don't pre-train whole model but run small experiment.",
    )

    args = parser.parse_args()

    config = Config(args.config_path)

    if args.lr is not None:
        config["lr"] = args.lr
    if args.data_path is not None:
        config["data_path"] = args.data_path
    if args.init_factor is not None:
        config["perturb_init_factor"] = args.init_factor
    if args.batch_size is not None:
        config["batch_size"] = args.batch_size

    dm = BentoDataModule(config)
    dm.setup(None)

    model = PerturbTransformer(config)
    pretrained_model = BentoTransformer.load_from_checkpoint(args.checkpoint)

    pretrained_dict = pretrained_model.state_dict()
    model_dict = model.state_dict()
    pretrained_dict_new = {
        k: v
        for k, v in pretrained_dict.items()
        if not k.startswith(("nce_loss", "ct_clf_loss", "loss"))
    }
    model_dict.update(pretrained_dict_new)
    model.load_state_dict(model_dict)

    val_ckpt = ModelCheckpoint(monitor="val_deltapearson", mode="max")
    callbacks = [
        val_ckpt,
        EarlyStopping(monitor="val_deltapearson", patience=40, mode="max"),
    ]

    logger = TensorBoardLogger(
        "/".join(args.logs_path.split("/")[:-1]),
        name=args.logs_path.split("/")[-1],
    )

    if args.tune_mode:
        max_steps = (
            int(5_000 // (config.batch_size / 32)) + 1
        )  # actual steps, so taking into account acc grad
        val_check_interval = int(
            400 // (config.batch_size / 32) ** 0.5
        )  # in practice one in every 100
    else:
        max_steps = (
            int(50_000 // (config.batch_size / 32)) + 1
        )  # actual steps, so taking into account acc grad
        val_check_interval = int(
            2_000 // (config.batch_size / 32) ** 0.5
        )  # in practice results in one every 500 with acc grad batches

    trainer = Trainer(
        accelerator="gpu",
        devices=config.devices,
        strategy="auto",
        plugins=[LightningEnvironment()],
        gradient_clip_val=1,
        max_steps=max_steps,
        val_check_interval=val_check_interval,
        check_val_every_n_epoch=None,
        callbacks=callbacks,
        logger=logger,
        precision="bf16-true",
        use_distributed_sampler=(True if config.return_zeros else False),
        accumulate_grad_batches=4,
    )

    trainer.fit(model, dm.train_dataloader(), dm.val_dataloader())

    res = trainer.validate(model, dm.val_dataloader(), ckpt_path="best")
    print(res)
    dm.test.sample_processor.deterministic = True
    res = trainer.validate(model, dm.test_dataloader(), ckpt_path="best")
    print(res)


if __name__ == "__main__":
    main()
