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
        self.image_shape = [120, 160, 3]
        self.serial_port = "/dev/ttyUSB0"
        self.server_address = "ws://localhost:3000"

        self.logs_level = "debug"
        self.do_send_telemetry = True
        self.telemetry_delay = 0.03

        self.profiler_reset = False
        self.profiler_n_iter = 100
        self.profiler_filters = ["autopylot"]
        self.profiler_sort_by = "cumulative"
        pass

    def setattr(self, key, value):
        """Change the value of the attribute.

        Args:
            key (string): the key to set.
            value (any): the value.
        """
        setattr(self, key, value)

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
        map(self.setattr, settings_dict.items())

    def to_json(self, filepath):
        """Saves the settings dictionary to a json file.

        Args:
            filepath (string): path of the json file to load.
        """
        with open(filepath, "w") as f:
            json.dump(self.__dict__, f, indent=4)


try:
    settings = Settings()
    # settings.__generate_class_from_json(pathsettings)
    settings.from_json(pathsettings)
    settings.to_json(pathsettings)
except Exception:
    raise ValueError(
        "Could not load and save settings from json, please check your settings file."
    )
