"""
DevConf - Demo
"""

import numpy as np

from autopylot.actuators import Actuator
from autopylot.cameras import Camera
from autopylot.controllers import Controller
from autopylot.models import utils
from autopylot.utils import logger, memory, settings, vis


# init logger, memory, settings
logger.init()
mem = memory.mem
settings = settings.settings

# load model
model, model_info = utils.load_model(
    f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
)

# init actuators, cameras, controllers
actuator = Actuator()
camera = Camera()
controller = Controller()
logger.logging.info("Starting main loop")

# main loop
running = True
while running:
    try:
        camera.update()  # get the last frame from the camera
        controller.update()  # update keyboard inputs

        # get predictions
        predictions = model.predict(mem)

        # manual mode
        if mem["controller"]["button_x"]:
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]
            mem["brake"] = mem["controller"]["brake"]

        # autonomous
        else:
            mem["steering"] = predictions["steering.0"]
            mem["throttle"] = (
                np.matmul(predictions["zone"], settings.LOOKUP_ZONE)
                * settings.THROTTLE_MULT
            )
            mem["brake"] = 0.0

        # update actuators
        actuator.update()

        # visualize the image
        vis_image = vis.vis_all(mem)
        vis.show(vis_image)

    except KeyboardInterrupt:
        running = False
