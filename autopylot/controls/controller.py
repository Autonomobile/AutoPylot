# script based on https://github.com/autorope/donkeycar/blob/dev/donkeycar/parts/controller.py

import os
import struct
import array
import threading


class Joystick(object):
    """An interface to a physical joystick."""

    def __init__(self, dev_fn="/dev/input/js0"):
        """Init class."""
        self.axis_states = {}
        self.button_states = {}
        self.axis_names = {}
        self.button_names = {}
        self.axis_map = []
        self.button_map = []
        self.jsdev = None
        self.dev_fn = dev_fn
        self.connected = False

    def init(self):
        try:
            from fcntl import ioctl
        except ModuleNotFoundError:
            self.num_axes = 0
            self.num_buttons = 0
            print("no support for fnctl module. joystick not enabled.")
            return False

        if not os.path.exists(self.dev_fn):
            print(self.dev_fn, "is missing")
            return False

        """
        call once to setup connection to device and map buttons
        """
        # Open the joystick device.
        print("Opening %s..." % self.dev_fn)
        self.jsdev = open(self.dev_fn, "rb")

        # Get the device name.
        buf = array.array("B", [0] * 64)
        # JSIOCGNAME(len)
        ioctl(self.jsdev, 0x80006A13 + (0x10000 * len(buf)), buf)
        self.js_name = buf.tobytes().decode("utf-8")
        print("Device name: %s" % self.js_name)

        # Get number of axes and buttons.
        buf = array.array("B", [0])
        ioctl(self.jsdev, 0x80016A11, buf)  # JSIOCGAXES
        self.num_axes = buf[0]

        buf = array.array("B", [0])
        ioctl(self.jsdev, 0x80016A12, buf)  # JSIOCGBUTTONS
        self.num_buttons = buf[0]

        # Get the axis map.
        buf = array.array("B", [0] * 0x40)
        ioctl(self.jsdev, 0x80406A32, buf)  # JSIOCGAXMAP

        for axis in buf[: self.num_axes]:
            axis_name = self.axis_names.get(axis, "unknown(0x%02x)" % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0.0

        # Get the button map.
        buf = array.array("H", [0] * 200)
        ioctl(self.jsdev, 0x80406A34, buf)  # JSIOCGBTNMAP

        for btn in buf[: self.num_buttons]:
            btn_name = self.button_names.get(btn, "unknown(0x%03x)" % btn)
            self.button_map.append(btn_name)
            self.button_states[btn_name] = 0
            # print('btn', '0x%03x' % btn, 'name', btn_name)

        self.connected = True

        th = threading.Thread(target=self.poll)
        th.start()

        return True

    def show_map(self):
        """List the buttons and axis found on this joystick."""
        print("%d axes found: %s" % (self.num_axes, ", ".join(self.axis_map)))
        print("%d buttons found: %s" % (self.num_buttons, ", ".join(self.button_map)))

    def poll(self):
        """Query the state of the joystick, returns button which was pressed.

        button_state will be None, 1, or 0 if no changes,
        pressed, or released. axis_val will be a float from -1 to +1. button and axis will
        be the string label determined by the axis map in init.
        """
        evbuf = None

        while self.connected:
            if self.jsdev is None:
                break

            try:
                evbuf = self.jsdev.read(8)
            except OSError:
                self.connected = False
                break

            if evbuf:
                tval, value, typev, number = struct.unpack("IhBB", evbuf)

                if typev & 0x80:
                    # ignore initialization event
                    pass

                if typev & 0x01:
                    button = self.button_map[number]
                    # print(tval, value, typev, number, button, 'pressed')
                    if button:
                        self.button_states[button] = value

                if typev & 0x02:
                    axis = self.axis_map[number]
                    if axis:
                        fvalue = value / 32767.0
                        self.axis_states[axis] = fvalue

        print("Controller stopped")


class XboxOneJoystick(Joystick):
    """An interface to a physical joystick 'Xbox Wireless Controller' controller.
    This will generally show up on /dev/input/js0.
    - Note that this code presumes the built-in linux driver for 'Xbox Wireless Controller'.
      There is another user land driver called xboxdrv; this code has not been tested
      with that driver.
    - Note that this controller requires that the bluetooth disable_ertm parameter
      be set to true; to do this:
      - edit /etc/modprobe.d/xbox_bt.conf
      - add the line: options bluetooth disable_ertm=1
      - reboot to tha this take affect.
      - after reboot you can vertify that disable_ertm is set to true entering this
        command oin a terminal: cat /sys/module/bluetooth/parameters/disable_ertm
      - the result should print 'Y'.  If not, make sure the above steps have been done corretly.

    credit:
    https://github.com/Ezward/donkeypart_ps3_controller/blob/master/donkeypart_ps3_controller/part.py
    """

    def __init__(self, memory, *args, **kwargs):
        """Controller class init"""
        super(XboxOneJoystick, self).__init__(*args, **kwargs)

        self.memory = memory

        self.axis_names = {
            0x00: "x",
            0x01: "y",
            0x02: "z",
            0x03: "rx",
            0x04: "ry",
            0x05: "rz",
            0x10: "hat0x",
            0x11: "hat0y",
            0x12: "hat1x",
            0x13: "hat1y",
        }

        self.button_names = {
            0x130: "a",
            0x131: "b",
            0x133: "x",
            0x134: "y",
            0x13A: "back",
            0x13B: "start",
            0x136: "lb",
            0x137: "rb",
        }

    def update(self):
        """Update function for the controller.

        This function stores in the memory the newly fetched axis values.
        """
        # calculate the steering and throttle now st we don't need to reprocess them
        # steering = self.axis_states['x']
        # throttle = self.joy.axis_states["rz"] - self.joy.axis_states["z"]

        # provide steering, throttle and every axis/buttons values we have
        self.memory["controller"] = {**self.axis_states, **self.button_states}
