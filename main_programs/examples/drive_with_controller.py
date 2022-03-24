from autopylot.cameras import Camera
from autopylot.actuators import Actuator
from autopylot.controllers import Controller
from autopylot.utils import logger, memory, state_switcher

# init the logger handlers
logger.init()

mem = memory.mem

state_switcher_cls = state_switcher.StateSwitcher()
actuator = Actuator()
camera = Camera()
controller = Controller()


def main():
    while True:

        controller.update()  # update joystick

        # state_switcher_cls.update()  # car state
        camera.update()  # get the last frame from the camera

        # if mem["state"] == "stop":
        #     mem["steering"] = 0.0
        #     mem["throttle"] = 0.0

        # elif mem["state"] == "manual":
        #     mem["steering"] = mem["controller"]["steering"]
        #     mem["throttle"] = mem["controller"]["throttle"]

        # elif mem["state"] == "autonomous":
        #     mem["steering"] = 0.0
        #     mem["throttle"] = 0.0

        # elif mem["state"] == "collect":
        #     mem["steering"] = mem["controller"]["steering"]
        #     mem["throttle"] = mem["controller"]["throttle"]

        mem["steering"] = mem["controller"]["steering"]
        mem["throttle"] = mem["controller"]["throttle"]

        actuator.update()


if __name__ == "__main__":
    main()
