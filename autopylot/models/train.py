"""Train a model with a given dataset."""
import logging
import os
import random

from ..datasets import datagenerator, dataset
from ..utils import settings
from . import architectures, utils, info_parser

settings = settings.settings


class TrainModel:
    """Class to train a model."""

    def __init__(
        self,
        name=settings.MODEL_NAME,
        try_load=settings.TRAIN_LOAD_MODEL,
        model_type=architectures.Models.test_model,
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
                    self.model, self.model_info = utils.load_model(
                        f"{self.name}/{self.name}.h5"
                    )
                    logging.info("Loaded model")
                except ValueError:
                    self.model = model_type(*args, **kwargs)
                    self.model_info = utils.create_model_info(self.model)
                    logging.info("Failed loading model, created new one")
            else:
                self.model = model_type(*args, **kwargs)
                self.model_info = utils.create_model_info(self.model)
                logging.info("Created model")
        else:
            raise ValueError("model_type should be a function")

        if settings.TRAIN_FREEZE_CONV:
            utils.freeze_conv(self.model)
            logging.info("Freezed conv layers")

    def train(
        self,
        dataset_path=settings.DATASET_PATH,
        epochs=settings.TRAIN_EPOCHS,
        batch_size=settings.TRAIN_BATCH_SIZE,
        train_split=settings.TRAIN_SPLITS,
        shuffle=settings.TRAIN_SHUFFLE,
        verbose=settings.TRAIN_VERBOSE,
        do_save=True,
        additionnal_funcs=[],
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
            additionnal_funcs (list(tuple(method, float)), optional): tuple containing the function and the frequency.

        Raises:
            ValueError: raised if the train_split is not between 0 and 1.
            ValueError: raised if the dataset path is not valid.
        """
        if not 0 <= train_split <= 1:
            raise ValueError("train_split should be between 0 and 1")

        if not os.path.exists(dataset_path):
            raise ValueError(f"Dataset path {dataset_path} not found")

        # input parser
        infoParser = info_parser.InfoParser(self.model_info)
        logging.info(f"input / output order mapping: {infoParser.index_map}")

        seq_paths = dataset.sequence_sorted_paths(dataset_path)
        indexes = []
        for i, seq_path in enumerate(seq_paths):
            for j in range(0, len(seq_path) - infoParser.max_ahead):
                indexes.append((i, j))

        # shuffle the list of indexes
        if shuffle:
            random.shuffle(indexes)

        datalen = 0
        for seq_path in seq_paths:
            datalen += len(seq_path)

        train_idx = indexes[: int(datalen * train_split)]
        test_idx = indexes[int(datalen * train_split) :]

        logging.info(f"training model on {len(train_idx)} samples")

        # Create train and test datagenerators
        train_generator = datagenerator.DataGenerator(
            indexes=train_idx,
            paths=seq_paths,
            inp_out=infoParser.parsed,
            index_map=infoParser.index_map,
            batch_size=batch_size,
            additionnal_funcs=additionnal_funcs,
        )

        test_generator = datagenerator.DataGenerator(
            indexes=test_idx,
            paths=seq_paths,
            inp_out=infoParser.parsed,
            index_map=infoParser.index_map,
            batch_size=batch_size,
            additionnal_funcs=additionnal_funcs,
        )

        self.model.fit(
            train_generator,
            steps_per_epoch=len(train_generator) // batch_size + 1,
            validation_data=test_generator,
            validation_steps=len(test_generator) // batch_size + 1,
            epochs=settings.TRAIN_EPOCHS,
            max_queue_size=32,
            workers=16,
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
        utils.save_model(self.model, self.name, model_info=self.model_info)
