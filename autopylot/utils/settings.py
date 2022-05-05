import logging
import json
import os
import sys

pathsettings = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "settings.json",
)


class Settings:
    """Settings class for storing settings in the project."""

    def __init__(self):
        """Init of the Settings class."""

        # Telemetry settings
        self.LOG_LEVEL = "info"
        self.DO_SEND_TELEMETRY = True
        self.TELEMETRY_DELAY = 0.03

        # Core settings
        self.IMAGE_SHAPE = [120, 160, 3]
        self.CAMERA_TYPE = "webcam"  # "sim" / "dummy" / "replay"
        self.ACTUATOR_TYPE = "serial"  # "sim"
        self.CONTROLLER_TYPE = "xbox"  # "keyboard"
        self.JSON_FILE_FORMAT = "{t}.json"

        # Sim settings
        self.SIM_HOST = "127.0.0.1"
        self.SIM_PORT = 9091

        # Serial settings
        self.SERIAL_PORT = "/dev/ttyUSB0"
        self.SERVER_ADDRESS = "ws://localhost:3000"

        self.PROFILER_RESET = False
        self.PROFILER_N_ITER = 100
        self.PROFILER_FILTERS = ["autopylot"]
        self.PROFILER_SORT_BY = "cumulative"

        self.KEYMAP = {
            "forward": "z",
            "backward": "s",
            "left": "q",
            "right": "d",
            "recording": "r",
        }

        # Model settings
        self.MODEL_TYPE = "steering_model"
        self.MODEL_NAME = "exotic"
        self.MODEL_SAVE_SETTINGS = True

        # Training settings
        self.TRAIN_LOAD_MODEL = False
        self.TRAIN_BATCH_SIZE = 32
        self.TRAIN_EPOCHS = 10
        self.TRAIN_SPLITS = 0.9
        self.TRAIN_SHUFFLE = True
        self.TRAIN_VERBOSE = 1

        # transform functions
        self.ENABLE_TRANSFORM = True
        self.TRANSFORM_FUNCTIONS = {
            "flip": 0.5,
            "brightness": 0.2,
            "shift": 0.2,
            "shadow": 0.2,
            "blur": 0.2,
            "noise": 0.2,
            "bilateral_filter": 0.2,
        }

        # Paths
        self.ROOT_PATH = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.MODELS_PATH = os.path.join(self.ROOT_PATH, "models")
        self.LOGS_PATH = os.path.join(self.ROOT_PATH, "logs", "logs.log")
        self.PROFILER_PATH = os.path.join(self.ROOT_PATH, "logs", "profiler.log")
        self.COLLECT_PATH = os.path.normpath(os.path.expanduser("~/collect/"))
        self.DATASET_PATH = os.path.normpath(os.path.expanduser("~/datasets/"))

        if not os.path.exists(self.COLLECT_PATH):
            os.mkdir(self.COLLECT_PATH)
        if not os.path.exists(self.DATASET_PATH):
            os.mkdir(self.DATASET_PATH)

    def setattr(self, key, value):
        """Change the value of the attribute.

        Args:
            key (string): the key to set.
            value (any): the value.
        """
        self.__setattr__(key, value)

    def __generate_class_from_json(self, filepath):
        """This modifies the class properties from a json file.
        DO NOT USE THIS FUNCTION IN PRODUCTION !

        Args:
            filepath (string): path of the json file to load.
        """
        settings_dict = json.load(open(filepath))

        filepath = os.path.abspath(__file__)
        with open(filepath, "r") as f:
            lines = f.readlines()

        with open(filepath, "w") as f:
            for line in lines:
                # insert here the lines
                if line == "        pass\n":
                    for key, value in settings_dict.items():
                        if getattr(self, key, None) is None:
                            f.write(f"        self.{key} = {value}\n")
                f.write(line)

    def from_json(self, filepath=pathsettings):
        """Loads values from a json file.

        Args:
            filepath (string): path of the json file to load.
        """
        settings_dict = json.load(open(filepath))
        for key, value in settings_dict.items():
            self.setattr(key, value)

    def to_json(self, filepath=pathsettings):
        """Saves the settings dictionary to a json file.

        Args:
            filepath (string): path of the json file to load.
        """
        with open(filepath, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def update(self, settings: dict):
        """Update the settings with a dictionary.

        Args:
            settings (dict): the settings to update.
        """
        for key, value in settings.items():
            self.setattr(key, value)

    def __repr__(self):
        return self.__dict__.__repr__()


def restart_car():
    """save settings and reload the car."""
    settings.to_json()
    logging.info("Restarting car")

    python = sys.executable
    os.execl(python, python, *sys.argv)


try:
    settings = Settings()
    if os.path.exists(pathsettings):
        # settings.__generate_class_from_json(pathsettings)
        settings.from_json()
        settings.to_json()
        logging.info(f"Loaded settings from {pathsettings}")
    else:
        settings.to_json()
        logging.info(f"Created settings.json at {pathsettings}")
except Exception as e:
    raise ValueError(
        f"Could not load and save settings from json, please check your settings file. {e}"
    )
