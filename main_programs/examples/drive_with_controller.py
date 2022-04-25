import os
import time

import numpy as np
from autopylot.actuators import Actuator
from autopylot.cameras import Camera
from autopylot.controllers import Controller
from autopylot.datasets import preparedata, transform
from autopylot.models import utils
from autopylot.utils import io, logger, memory, settings, state_switcher

# init the logger handlers
logger.init()

mem = memory.mem
settings = settings.settings

model, model_info = utils.load_model(
    f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
)
prepare_data = preparedata.PrepareData(model_info)

settings.ENABLE_TRANSFORM = False
transformers = transform.Transform()

# set dataset paths
if not os.path.exists(settings.COLLECT_PATH):
    os.mkdir(settings.COLLECT_PATH)

sw = state_switcher.StateSwitcher()
actuator = Actuator()
camera = Camera()
controller = Controller()

lookup_zone = [0.6, 0.3, -1.0]
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
            transformers(mem)
            input_data = prepare_data(mem)
            predictions = model.predict(input_data)

            if "zone" in predictions.keys():
                zone_idx = np.argmax(predictions["zone"])
                if zone_idx == 0:
                    throttle = lookup_zone[0] * predictions["zone"][0]
                elif zone_idx == 1:
                    throttle = (
                        lookup_zone[1] * predictions["zone"][1]
                        + lookup_zone[0] * predictions["zone"][0]
                    )
                else:
                    throttle = (
                        lookup_zone[2] * predictions["zone"][2]
                        if mem["speed"] > min_speed
                        else lookup_zone[1]
                    )

            else:
                throttle = 0.2

            mem["steering"] = float(predictions["steering"]) * 1.0
            mem["throttle"] = throttle

            io.save_image_data(
                mem,
                os.path.join(
                    settings.COLLECT_PATH,
                    settings.JSON_FILE_FORMAT.format(t=time.time()),
                ),
            )

        elif mem["state"] == "collect":
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]

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
