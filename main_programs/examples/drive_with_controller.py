import os
import time

from autopylot.actuators import Actuator
from autopylot.cameras import Camera
from autopylot.controllers import Controller
from autopylot.utils import io, logger, memory, settings, state_switcher

# init the logger handlers
logger.init()

mem = memory.mem
settings = settings.settings

# set dataset paths
settings.DATASET_PATH = os.path.expanduser(settings.DATASET_PATH)
if not os.path.exists(settings.DATASET_PATH):
    os.mkdir(settings.DATASET_PATH)

sw = state_switcher.StateSwitcher()
actuator = Actuator()
camera = Camera()
controller = Controller()


def main():
    while True:
        camera.update()  # get the last frame from the camera
        controller.update()  # update joystick
        sw.update()  # car state

        if mem["state"] == "stop":
            mem["steering"] = 0.0
            mem["throttle"] = 0.0

        elif mem["state"] == "manual":
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]

        elif mem["state"] == "autonomous":
            mem["steering"] = 0.0
            mem["throttle"] = 0.0

        elif mem["state"] == "collect":
            io.save_image_data(
                mem,
                os.path.join(
                    settings.DATASET_PATH,
                    settings.JSON_FILE_FORMAT.format(t=time.time()),
                ),
            )
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]

        mem["steering"] = mem["controller"]["steering"]
        mem["throttle"] = mem["controller"]["throttle"]

        actuator.update()


if __name__ == "__main__":
    main()
