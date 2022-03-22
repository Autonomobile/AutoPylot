from autopylot.cameras import camera
from autopylot.controls import controller, control, state_switcher
from autopylot.utils import logger, memory

# init the logger handlers
logger.init()

mem = memory.mem

state = state_switcher.StateSwitcher()
serial = control.Control()
cam = camera.Camera()
js = controller.Controller()


def main():
    while True:

        js.update()  # update joystick

        # state.update()  # car state
        cam.update()  # get the last frame from the camera

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

        serial.update()  # send commands to the memory


if __name__ == "__main__":
    main()
