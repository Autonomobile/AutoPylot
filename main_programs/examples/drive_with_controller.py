import os
import time

from autopylot.actuators import Actuator
from autopylot.cameras import Camera
from autopylot.controllers import Controller
from autopylot.utils import io, logger, memory, settings, state_switcher
from autopylot.models import utils
from autopylot.datasets import preparedata

# init the logger handlers
logger.init()

mem = memory.mem
settings = settings.settings

model, model_info = utils.load_model(
    f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
)
prepare_data = preparedata.PrepareData(model_info)

# set dataset paths
if not os.path.exists(settings.COLLECT_PATH):
    os.mkdir(settings.COLLECT_PATH)

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
            input_data = prepare_data(mem)
            predictions = model.predict(input_data)
            mem.update(predictions)
            mem["steering"] *= 3
            mem["throttle"] = 0.35

        elif mem["state"] == "collect":
            io.save_image_data(
                mem,
                os.path.join(
                    settings.COLLECT_PATH,
                    settings.JSON_FILE_FORMAT.format(t=time.time()),
                ),
            )
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]

        actuator.update()


if __name__ == "__main__":
    main()
