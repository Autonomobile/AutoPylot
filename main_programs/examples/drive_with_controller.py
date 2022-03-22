from autopylot.cameras import camera
from autopylot.controls import control
from autopylot.controllers import controller
from autopylot.utils import logger, memory, state_switcher

# init the logger handlers
logger.init()

mem = memory.mem

state_switcher_cls = state_switcher.StateSwitcher()
control_cls = control.Control()
camera_cls = camera.Camera()
controller_cls = controller.Controller()


def main():
    while True:

        controller_cls.update()  # update joystick

        # state_switcher_cls.update()  # car state
        camera_cls.update()  # get the last frame from the camera

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

        control_cls.update()


if __name__ == "__main__":
    main()
