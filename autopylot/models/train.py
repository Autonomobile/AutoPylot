"""Train a model with a given dataset."""
import os
import random

from ..datasets import datagenerator, dataset
from ..utils import settings
from . import architectures, utils

settings = settings.settings


class TrainModel:
    """Class to train a model."""

    def __init__(
        self,
        name=settings.MODEL_NAME,
        try_load=settings.TRAIN_LOAD_MODEL,
        model_type=architectures.test_model,
        *args,
        **kwargs,
    ):
        """Init of the class.

        Args:
            name (str, optional): name of the model. Defaults to settings.MODEL_NAME.
            model_type (callable, optional): method to create the model. Defaults to architectures.test_model.

        Raises:
            ValueError: raise an error if the model type is not supported.
        """
        self.name = name

        if callable(model_type):
            if try_load:
                try:
                    self.model, self.model_info = utils.load_model(self.name)
                except ValueError:
                    self.model = model_type(*args, **kwargs)
                    self.model_info = utils.create_model_info(self.model)
            else:
                self.model = model_type(*args, **kwargs)
                self.model_info = utils.create_model_info(self.model)
        else:
            raise ValueError("model_type should be a function")

    def train(
        self,
        dataset_path=settings.DATASET_PATH,
        epochs=settings.TRAIN_EPOCHS,
        batch_size=settings.TRAIN_BATCH_SIZE,
        train_split=settings.TRAIN_SPLITS,
        shuffle=settings.TRAIN_SHUFFLE,
        verbose=settings.TRAIN_VERBOSE,
        augm_freq=settings.TRAIN_AUGM_FREQ,
        do_save=True,
    ):
        """Trains the model on the given dataset.

        Args:
            dataset_path (str, optional): path to the dataset. Defaults to settings.DATASET_PATH.
            epochs (int, optional): number of epochs. Defaults to settings.TRAIN_EPOCHS.
            batch_size (int, optional): number of samples per batch. Defaults to settings.TRAIN_BATCH_SIZE.
            train_split (float, optional): ratio of the dataset to split. Defaults to settings.TRAIN_SPLITS.
            shuffle (bool, optional): shuffle the dataset. Defaults to settings.TRAIN_SHUFFLE.
            verbose (bool, optional): print verbose messages. Defaults to settings.TRAIN_VERBOSE.
            do_save (bool, optional): save the model. Defaults to True.

        Raises:
            ValueError: raised if the train_split is not between 0 and 1.
            ValueError: raised if the dataset path is not valid.
        """
        if not 0 <= train_split <= 1:
            raise ValueError("train_split should be between 0 and 1")

        if not os.path.exists(dataset_path):
            raise ValueError(f"Dataset path {dataset_path} not found")

        paths = dataset.sort_paths(dataset.get_every_json_paths(dataset_path))

        # shuffle the list of paths
        if shuffle:
            random.shuffle(paths)

        datalen = len(paths)
        train_paths = paths[: int(datalen * train_split)]
        test_paths = paths[int(datalen * train_split) :]

        inputs = [i[0] for i in self.model_info["inputs"]]
        outputs = [i[0] for i in self.model_info["outputs"]]

        # Create train and test datagenerators
        train_generator = datagenerator.DataGenerator(
            paths=train_paths,
            inputs=inputs,
            outputs=outputs,
            freq=augm_freq,
        )

        test_generator = datagenerator.DataGenerator(
            paths=test_paths,
            inputs=inputs,
            outputs=outputs,
            freq=0.0,
        )

        self.model.fit(
            train_generator,
            steps_per_epoch=len(train_generator) // batch_size + 1,
            validation_data=test_generator,
            validation_steps=len(test_generator) // batch_size + 1,
            epochs=epochs,
            max_queue_size=8,
            workers=4,
        )

        if settings.MODEL_SAVE_SETTINGS:
            self.model_info["settings"] = {
                "dataset_path": dataset_path,
                "epochs": epochs,
                "batch_size": batch_size,
                "train_split": train_split,
                "shuffle": shuffle,
                "verbose": verbose,
            }
        if do_save:
            utils.save_model(self.model, self.name, model_info=self.model_info)
