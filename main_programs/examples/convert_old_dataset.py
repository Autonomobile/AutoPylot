"""Convert old dataset format to new format.
"""

from autopylot.datasets import dataset
from autopylot.utils import settings, io


settings = settings.settings


def main(dataset_path):
    for path in dataset.get_every_json_paths(dataset_path):
        data = io.load_json(path)
        if "direction" in data.keys():
            data["steering"] = data["direction"]
            del data["direction"]
            io.save_json(path, data)


if __name__ == "__main__":
    main(settings.DATASET_PATH)
