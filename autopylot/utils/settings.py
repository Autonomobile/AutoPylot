import logging
import json
import os

pathsettings = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "settings.json",
)


class Settings:
    """Settings class for storing settings in the project."""

    def __init__(self):
        """Init of the Settings class."""
        self.LOG_LEVEL = "info"
        self.DO_SEND_TELEMETRY = True
        self.TELEMETRY_DELAY = 0.03

        self.IMAGE_SHAPE = [120, 160, 3]
        self.CAMERA_TYPE = "webcam"  # "sim" / "dummy" / "replay"
        self.ACTUATOR_TYPE = "serial"  # "sim"
        self.CONTROLLER_TYPE = "xbox"  # "keyboard"
        self.DATASET_PATH = "~/collect/"
        self.JSON_FILE_FORMAT = "{t}.json"

        self.SIM_HOST = "127.0.0.1"
        self.SIM_PORT = 9091

        self.SERIAL_PORT = "/dev/ttyUSB0"
        self.SERVER_ADDRESS = "ws://localhost:3000"

        self.PROFILER_RESET = False
        self.PROFILER_N_ITER = 100
        self.PROFILER_FILTERS = ["autopylot"]
        self.PROFILER_SORT_BY = "cumulative"

        pass

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

    def from_json(self, filepath):
        """Loads values from a json file.

        Args:
            filepath (string): path of the json file to load.
        """
        settings_dict = json.load(open(filepath))
        for key, value in settings_dict.items():
            self.setattr(key, value)

    def to_json(self, filepath):
        """Saves the settings dictionary to a json file.

        Args:
            filepath (string): path of the json file to load.
        """
        with open(filepath, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def __repr__(self):
        return self.__dict__.__repr__()


try:
    settings = Settings()
    if os.path.exists(pathsettings):
        # settings.__generate_class_from_json(pathsettings)
        settings.from_json(pathsettings)
        settings.to_json(pathsettings)
        logging.info(f"Loaded settings from {pathsettings}")
    else:
        settings.to_json(pathsettings)
        logging.info(f"Created settings.json at {pathsettings}")
except Exception as e:
    raise ValueError(
        f"Could not load and save settings from json, please check your settings file. {e}"
    )
