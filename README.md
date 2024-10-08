[![License: BSD-3](https://img.shields.io/badge/License-BSD3-blue.svg)](https://opensource.org/license/bsd-3-clause)
[![PyPI](https://img.shields.io/pypi/v/spotiflow.svg?color=green)](https://pypi.org/project/spotiflow)
[![Python Version](https://img.shields.io/pypi/pyversions/spotiflow.svg?color=green)](https://python.org)
[![tests](https://github.com/weigertlab/spotiflow/workflows/tests/badge.svg)](https://github.com/weigertlab/spotiflow/actions)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/spotiflow)](https://pypistats.org/packages/spotiflow)

![Logo](artwork/spotiflow_logo.png)
---




# Spotiflow - accurate and efficient spot detection with stereographic flow

*Spotiflow* is a deep learning-based, threshold-agnostic, subpixel-accurate 2D and 3D spot detection method for fluorescence microscopy. It is primarily developed for spatial transcriptomics workflows that require transcript detection in large, multiplexed FISH-images, although it can also be used to detect spot-like structures in general fluorescence microscopy images and volumes. A more detailed description of the method can be found in [our paper](https://doi.org/10.1101/2024.02.01.578426).

![Overview](artwork/overview.png)

The documentation of the software can be found [here](https://weigertlab.github.io/spotiflow/).

## Installation (pip, recommended)
Create and activate a fresh conda environment (we currently support Python 3.9 to 3.11):

```console
conda create -n spotiflow python=3.9
conda activate spotiflow
```


**Note (for MacOS users):** if using MacOS, there is a known bug causing the installation of PyTorch with `conda` to sometimes break OpenMP. You can avoid installing PyTorch with `conda` and let spotiflow install it automatically via `pip` instead.

For Linux/Windows with a CUDA device, install PyTorch using conda/mamba (one might need to change the cuda version accordingly):
```console
conda install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia # Might need to change the cuda version accordingly
```

**Note (for Windows users):** if using Windows, please install the latest [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) (make sure to select the C++ build tools during installation) before proceeding to install Spotiflow.


Finally, install `spotiflow`:

```console
pip install spotiflow
```

## Installation (conda)
For Linux/MacOS users, you can also install Spotiflow using conda through the `conda-forge` channel:

```console
conda install -c conda-forge spotiflow
```

The conda package is, for now, not CUDA-compatible. We recommend using `pip` to install Spotiflow if available.

## Usage

### Training (2D images)
See the [example training script](scripts/train.py) or the [example notebook](examples/1_train.ipynb) for an example of training. For finetuning an already pretrained model, please refer to the [finetuning example notebook](examples/3_finetune.ipynb).

### Training (3D volumes)
See the [example 3D training script](scripts/train_simple_3d.py). For more information, please refer to the [3D training example notebook](examples/4_train_3d.ipynb). Fine-tuning a 3D model can be done by following the same workflow as to the 2D case.

### Inference (CLI)

You can use the CLI to run inference on an image or folder containing several images. To do that, you can use the following command:

```console
spotiflow-predict PATH
```

where PATH can be either an image or a folder. By default, the command will use the `general` pretrained model. You can specify a different model by using the `--pretrained-model` flag. Moreover, spots are saved to a subfolder `spotiflow_results` created inside the input folder (this can be changed with the `--out-dir` flag). For more information, please refer to the help message of the CLI (`$ spotiflow-predict -h`).

### Inference (Docker)

Alternatively to installing Spotiflow as command line tool on your operating system, you can also use it directly from our Docker container (thanks to @migueLib for the contribution!). To do so, you can use the following command:

To pull the Docker container from Dockerhub use:
``` console
docker pull weigertlab/spotiflow:main
```

Then, run spotiflow-predict with:
```console
docker run -it -v [/local/input/folder]:/spotiflow/input weigertlab/spotiflow:main spotiflow-predict input/your_file.tif -o .
```
Where:  
`-v`: represents the volume flag, which allows you to mount a folder from your local machine to the container.    
`/path/to/your/data:/spotiflow`: is the path to the folder containing the image you want to analyze.

Note:
- The current implementation of Spotiflow in Docker only supports CPU inference.



### Inference (API)

The API allows detecting spots in a new image in a few lines of code! Please check the [corresponding example notebook](examples/2_inference.ipynb) and the documentation for a more in-depth explanation. The same procedure can be followed for 3D volumes.

```python
from spotiflow.model import Spotiflow
from spotiflow.sample_data import test_image_hybiss_2d

# Load sample image
img = test_image_hybiss_2d()
# Or any other image
# img = tifffile.imread("myimage.tif")

# Load a pretrained model
model = Spotiflow.from_pretrained("general")
# Or load your own trained model from folder
# model = Spotiflow.from_folder("./mymodel")

# Predict
points, details = model.predict(img) # points contains the coordinates of the detected spots, the attributes 'heatmap' and 'flow' of `details` contain the predicted full resolution heatmap and the prediction of the stereographic flow respectively (access them by `details.heatmap` or `details.flow`). Retrieved spot intensities are found in `details.intens`.
```

### Napari plugin
Our napari plugin allows detecting spots in 2D and 3D directly with an easy-to-use UI. See [napari-spotiflow](https://github.com/weigertlab/napari-spotiflow) for more information.


## For developers

We are open to contributions, and we indeed very much encourage them! Make sure that existing tests pass before submitting a PR, as well as adding new tests/updating the documentation accordingly for new features.

### Testing

First, clone the repository:
```console
git clone git@github.com:weigertlab/spotiflow.git
```

Then install the `testing` extras:

```console
cd spotiflow
pip install -e ".[testing]"
```

then run the tests:

```console
pytest -v --color=yes --cov=spotiflow
```

### Docs

Install the `docs` extras:

```console
pip install -e ".[docs]"
```

and then `cd` into the `docs` folder of the cloned repository and build them:
```console
cd spotiflow/docs
sphinx-build -M html source build
```

## How to cite
If you use this code in your research, please cite [the Spotiflow paper](https://doi.org/10.1101/2024.02.01.578426) (currently preprint):

```bibtex
@article {dominguezmantes24,
	author = {Dominguez Mantes, Albert and Herrera, Antonio and Khven, Irina and Schlaeppi, Anjalie and Kyriacou, Eftychia and Tsissios, Georgios and Skoufa, Evangelia and Santangeli, Luca and Buglakova, Elena and Durmus, Emine Berna and Manley, Suliana and Kreshuk, Anna and Arendt, Detlev and Aztekin, Can and Lingner, Joachim and La Manno, Gioele and Weigert, Martin},
	title = {Spotiflow: accurate and efficient spot detection for fluorescence microscopy with deep stereographic flow regression},
	elocation-id = {2024.02.01.578426},
	year = {2024},
	doi = {10.1101/2024.02.01.578426},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/early/2024/02/05/2024.02.01.578426},
	eprint = {https://www.biorxiv.org/content/early/2024/02/05/2024.02.01.578426.full.pdf},
	journal = {bioRxiv}
}
```
