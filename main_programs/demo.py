"""
DevConf - Demo
"""

import numpy as np

from autopylot.actuators import Actuator
from autopylot.cameras import Camera
from autopylot.controllers import Controller
from autopylot.utils import logger, memory, settings, vis


# init logger, and memory
logger.init()
mem = memory.mem

settings = settings.settings
settings.CAMERA_TYPE = "sim"
settings.ACTUATOR_TYPE = "sim"
settings.CONTROLLER_TYPE = "keyboard"
settings.MODEL_NAME = "demo"

settings.SIM_HOST = "127.0.0.1"
settings.SIM_PORT = 9091

# load model
# model, model_info = utils.load_model(
#     f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
# )

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
        # predictions = model.predict(mem)

        # update memory
        # mem["steering"] = predictions["steering.0"]
        # mem["throttle"] = predictions["throttle.0"]
        # mem["brake"] = predictions["brake.0"]

        mem["steering"] = mem["controller"]["steering"]
        mem["throttle"] = mem["controller"]["throttle"] * 4
        mem["brake"] = mem["controller"]["brake"]

        # update actuators
        actuator.update()

        # visualize the image
        vis_image = vis.vis_all(mem["image"])
        vis.cv2.imshow("vis_image", vis_image)

    except KeyboardInterrupt:
        running = False

    except Exception as e:
        logger.logging.error(e)
        running = False

# close actuators
actuator.sim_client.close()
