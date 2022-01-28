from autopylot.controls import controller, state_switcher, serial_control
from autopylot.cameras import camera
from autopylot.utils import memory

mem = memory.Memory()

state = state_switcher.StateSwitcher(mem)
serial = serial_control.SerialControl(mem)
cam = camera.Camera(mem)
js = controller.XboxOneJoystick(mem)
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
        print(mem)


if __name__ == "__main__":
    main()
