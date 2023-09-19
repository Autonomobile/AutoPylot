"""
Before working with autopylot, which include training and predicting,
you need to setup the environment first. To do so, just run the following
command:

    python setup.py

!!! Make sure autopylot is installed !!!

it will generate a settings.json file in autopylot's root directory and
it will create $HOME/dataset and $HOME/collect directories.
"""

from setuptools import setup

setup(
    name="autopylot",
    version="0.0.1",
    description="An RC autonomous car python library",
    url="https://github.com/Autonomobile/AutoPylot",
    author="Autonomobile",
    license="MIT",
    packages=["autopylot"],
    install_requires=[
        "protobuf < 4.0.0rc1",
        "opencv-python >= 4.1.1",
        "tensorflow >= 2.3.0",
        "numpy >= 1.17",
        "matplotlib",
        "glob2",
        "pyserial",
        "python-socketio[client]",
        "gym-donkeycar @ git+https://github.com/Autonomobile/gym-donkeycar",
        "keyboard",
        "keras-flops",
        "numpy-quaternion",
        "tqdm",
        "psutil",
    ],
    extras_require={
        "dev": ["pytest", "flake8", "black", "pre-commit"],
        "test": ["pytest", "flake8"],
    },
)
