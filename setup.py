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
        "opencv-python >= 4.1.1",
        "tensorflow >= 2.3.0, <2.4",
        "numpy >= 1.17",
        "glob2",
        "pyserial",
        "python-socketio[client]",
        "gym-donkeycar @ git+https://github.com/tawnkramer/gym-donkeycar",
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
