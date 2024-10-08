"""Sample script to train a Spotiflow model.
"""

import argparse
import numpy as np
from pathlib import Path
from skimage import io
from itertools import chain

from spotiflow.model import Spotiflow, SpotiflowModelConfig
from spotiflow import utils
import lightning.pytorch as pl

IMAGE_EXTENSIONS = ("tif", "tiff", "png", "jpg", "jpeg")


def get_data(data_dir, multiclass=True):
    """Load data from data_dir."""
    img_files = sorted(tuple(chain(*tuple(data_dir.glob(f"*.{ext}") for ext in IMAGE_EXTENSIONS))))
    spots_files = sorted(data_dir.glob("*.csv"))

    images = tuple(io.imread(str(f)) for f in img_files)
    spots = tuple(utils.read_coords_csv(str(f), add_class_column=multiclass).astype(np.float32) for f in spots_files)
    return images, spots


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default="/data/spots/crosstalk/synth")
    parser.add_argument("--save-dir", type=Path, default="/data/tmp/crosstalk/multichannel_debug")
    parser.add_argument("--in-channels", type=int, default=4)
    parser.add_argument("--out-channels", type=int, default=4)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--debug", action="store_true", default=False)
    args = parser.parse_args()

    pl.seed_everything(args.seed, workers=True)

    print("Loading training data...")
    train_images, train_spots = get_data(args.data_dir / "train", multiclass=True)
    if args.debug:
        train_images, train_spots = train_images[:16], train_spots[:16]
    print(f"Training data loaded (N={len(train_images)}).")

    print("Loading validation data...")
    val_images, val_spots = get_data(args.data_dir / "val", multiclass=True)
    if args.debug:
        val_images, val_spots = val_images[:8], val_spots[:8]
    print(f"Validation data loaded (N={len(val_images)}).")

    if not args.skip_training:
        print("Instantiating model...")
        model = Spotiflow(
            SpotiflowModelConfig(
                in_channels=args.in_channels,
                out_channels=args.out_channels,
                sigma=args.sigma
            )
        )

        print("Launching training...")
        model.fit(
            train_images,
            train_spots,
            val_images,
            val_spots,
            save_dir=args.save_dir,
            device="auto",
            train_config={
                "num_epochs": args.epochs,
                "smart_crop": True,
            }
        )
        print("Done!")

    if not args.skip_testing:
        model = Spotiflow.from_folder(args.save_dir)
        test_images, test_spots = get_data(args.data_dir / "test", multiclass=True)
        if args.debug:
            test_images, test_spots = test_images[:8], test_spots[:8]
        print(f"Testing data loaded (N={len(test_images)}).")
        
