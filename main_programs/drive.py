import os
import time
import cv2
import numpy as np

from autopylot.actuators import Actuator
from autopylot.cameras import Camera
from autopylot.controllers import Controller
from autopylot.datasets import preparedata
from autopylot.models import utils
from autopylot.utils import io, logger, memory, settings, state_switcher

#########################################################################

logger.init()
mem = memory.mem
settings = settings.settings

model, model_info = utils.load_model(
    f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
)

if not os.path.exists(settings.COLLECT_PATH):
    os.mkdir(settings.COLLECT_PATH)

prepare_data = preparedata.PrepareData(model_info)
sw = state_switcher.StateSwitcher()
actuator = Actuator()
camera = Camera()
controller = Controller()

#########################################################################


def main():
    mem["speed"] = 0.0

    while True:
        camera.update()  # get the last frame from the camera
        controller.update()  # update joystick
        sw.update()  # car state

        if mem["state"] == "stop":
            mem["steering"] = 0.0
            mem["throttle"] = 0.0

        elif mem["state"] == "manual":
            mem["steering"] = (
                mem["controller"]["steering"] * settings.CONTROLLER_STEERING_MULT
            )
            mem["throttle"] = (
                mem["controller"]["throttle"] * settings.CONTROLLER_THROTTLE_MULT
            )

        elif mem["state"] == "autonomous":

            input_data = prepare_data(mem)
            predictions = model.predict(input_data)

            mem["steering"] = (
                (
                    predictions["steering.0"] * 1
                    + predictions["steering.10"] * 1
                    + predictions["steering.5"] * 1
                )
                / 3
                * settings.STEERING_MULT
            )

            if mem["speed"] < settings.MIN_SPEED:
                mem["throttle"] = settings.MIN_THROTTLE
            else:
                mem["throttle"] = (
                    np.matmul(predictions["zone"], settings.LOOKUP_ZONE)
                    * settings.THROTTLE_MULT
                )

        elif mem["state"] == "collect":
            mem["steering"] = mem["controller"]["steering"] * settings.STEERING_MULT
            mem["throttle"] = mem["controller"]["throttle"] * settings.THROTTLE_MULT

            io.save_image_data(
                mem,
                os.path.join(
                    settings.COLLECT_PATH,
                    settings.JSON_FILE_FORMAT.format(t=time.time()),
                ),
            )

        actuator.update()


if __name__ == "__main__":
    main()
