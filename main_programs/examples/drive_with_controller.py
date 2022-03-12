from autopylot.cameras import camera
from autopylot.controls import controller, serial_control, state_switcher
from autopylot.utils import logger, memory

# init the logger handlers
logger.init(send_telemetry=False)

mem = memory.mem

state = state_switcher.StateSwitcher()
serial = serial_control.SerialControl()
cam = camera.Camera()
js = controller.XboxOneJoystick()
js.init()


def main():
    while True:

        js.update()  # update joystick

        state.update()  # car state

        if mem["state"] == "stop":
            mem["steering"] = 0.0
            mem["throttle"] = 0.0

        elif mem["state"] == "manual":
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]

        elif mem["state"] == "autonomous":
            mem["steering"] = 0.0
            mem["throttle"] = 0.0

        elif mem["state"] == "collect":
            mem["steering"] = mem["controller"]["steering"]
            mem["throttle"] = mem["controller"]["throttle"]

            cam.update()  # get the last frame from the camera

        serial.update()  # send commands to the memory


if __name__ == "__main__":
    main()
