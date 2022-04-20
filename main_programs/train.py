"""Train a model using autopylot."""
from autopylot.models import train, architectures
from autopylot.utils import settings

settings = settings.settings


if __name__ == "__main__":
    trainer = train.TrainModel(
        name=settings.MODEL_NAME,
        try_load=settings.TRAIN_LOAD_MODEL,
        model_type=architectures.get_model_constructor_by_name(settings.MODEL_TYPE),
    )

    trainer.model.summary()

    trainer.train(
        dataset_path=settings.DATASET_PATH,
        epochs=settings.TRAIN_EPOCHS,
        batch_size=settings.TRAIN_BATCH_SIZE,
        train_split=settings.TRAIN_SPLITS,
        verbose=settings.TRAIN_VERBOSE,
        do_save=True,
    )
