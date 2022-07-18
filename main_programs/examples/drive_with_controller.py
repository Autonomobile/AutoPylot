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
transformers = transform.Transform()

# set dataset paths
if not os.path.exists(settings.COLLECT_PATH):
    os.mkdir(settings.COLLECT_PATH)

sw = state_switcher.StateSwitcher()
actuator = Actuator()
camera = Camera()
controller = Controller()

lookup_zone = [0.39, 0.32, 0.32]
min_speed = 1.75


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
            mem["steering"] = mem["controller"]["steering"] * settings.STEERING_MULT
            mem["throttle"] = mem["controller"]["throttle"] * settings.THROTTLE_MULT

        elif mem["state"] == "autonomous":
            transformers(mem)
            predictions = model.predict(mem)

            if "throttle" in predictions.keys():
                throttle = predictions["throttle"]
            elif "zone" in predictions.keys():
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
                throttle = settings.THROTTLE

            mem["steering"] = (
                float(predictions.get("steering", 0.0)) * settings.STEERING_MULT
            )
            mem["throttle"] = throttle * settings.THROTTLE_MULT

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
