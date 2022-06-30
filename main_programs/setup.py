"""
Before working with autopylot, which include training and predicting,
you need to setup the environment first. To do so, just run the following
command:

    python setup.py

!!! Make sure autopylot is installed !!!

it will generate a settings.json file in autopylot's root directory and
it will create $HOME/dataset and $HOME/collect directories.
"""
from autopylot.utils import settings
