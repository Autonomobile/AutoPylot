import os
import time

import numpy as np
from autopylot.actuators import Actuator
from autopylot.cameras import Camera
from autopylot.controllers import Controller
from autopylot.datasets import transform
from autopylot.models import utils
from autopylot.utils import io, logger, memory, settings, state_switcher

# init the logger handlers
logger.init()

mem = memory.mem
settings = settings.settings

model, model_info = utils.load_model(
    f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
)

settings.ENABLE_TRANSFORM = False
transform = transform.Transform()

# set dataset paths
if not os.path.exists(settings.COLLECT_PATH):
    os.mkdir(settings.COLLECT_PATH)

sw = state_switcher.StateSwitcher()
actuator = Actuator()
camera = Camera()
controller = Controller()

lookup_zone = [0.3, 0.3, 0.1]
min_speed = 1.75


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
            transform(mem)
            predictions = model.predict(mem)

            mem["steering"] = float(predictions["steering"]) * 1.0
            mem["throttle"] = 0.0

        elif mem["state"] == "collect":
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]

        actuator.update()


if __name__ == "__main__":
    main()
