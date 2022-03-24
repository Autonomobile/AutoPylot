"""Control the car using serial port."""
import logging
import threading
import time

import serial

from ..utils import memory, settings, utils


class SerialActuator:
    """This classs send through serial port commands to an Arduino to pilot a motors and a servo motor using PWM."""

    def __init__(
        self,
        memory=memory.mem,
        port=settings.settings.SERIAL_PORT,
        steering_key="steering",
        throttle_key="throttle",
        speed_key="speed",
    ):
        """Initialize the class.

        Args:
            memory (dict, optional): memory object.
            port (str, optional): serial port. Defaults to "/dev/ttyUSB0". example /dev/ttyS2 or /dev/ttyUSB0
            steering_key (str, optional): key of the steering in the memory. Defaults to "steering".
            throttle_key (str, optional): key of the throttle in the memory. Defaults to "throttle".
            speed_key (str, optional): key of the speed in the memory. Defaults to "speed".
        """
        if port == "loop://":
            # this one is for testing purposes
            self.ser = serial.serial_for_url("loop://")
        else:
            self.ser = serial.Serial()
            self.ser.port = port
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        self.ser.timeout = 0  # 0 = no timeout

        self.__sensor_rpm = 0  # init rpm of the sensor to 0
        self.__command = bytearray([255, 127, 127, 0])
        self.__isRuning = True
        self.__isOperation = False
        self.__boosting = False
        self.__toSend = []

        self.__memory = memory

        self.__steering_key = steering_key
        self.__throttle_key = throttle_key
        self.__speed_key = speed_key

        self.__ignore_next = False
        self.__steering = 127
        self.__throttle = 127
        self.__wheel_to_meters = 0.50  # 1 wheel turn = 0.20 m
        self.__gear_ratio = 7  # 7 motor turn = 1 wheel turn
        self.__last_received = time.time()

        try:
            if not self.ser.isOpen():
                self.ser.open()
                self.start_thread()

                # check which port was really used
                logging.info(f"Serial port {self.ser.portstr} opened")

        except Exception as e:
            logging.error(f"Error opening port: {e}")

    def stop(self):
        self.__isRuning = False
        self.__thread.join()
        if self.ser.is_open:
            self.apply_steering_throttle(0, 0)
            self.ser.close()  # close port

    def start_thread(self):
        self.__thread = threading.Thread(target=self.__run_threaded__)
        self.__thread.start()

    def __run_threaded__(self):
        while self.__isRuning:
            self.__read_rpm__()

    def __safe_write__(self, command):
        while self.__isOperation:
            pass
        self.__isOperation = True
        # print("writing", command)
        self.ser.write(command)
        self.__isOperation = False

    def __read_rpm__(self):
        if self.ser.in_waiting >= 1:
            while self.__isOperation:
                pass
            self.__isOperation = True
            try:
                out = self.ser.readlines()[-1]
                self.__decode_out__(out)

            finally:
                self.__isOperation = False

    def __decode_out__(self, out):
        if self.__ignore_next:
            self.__ignore_next = False

        else:
            # make sure that both end of lines are present
            if out != "" and out.endswith(b"\r\n"):
                res = int(out.decode())
                if 134 > self.__throttle > 120 and res > 27000:
                    self.__sensor_rpm = 0
                else:
                    self.__sensor_rpm = 30000000 / res
                # print(self.__throttle, res)

                self.__last_received = time.time()
                self.__memory[self.__speed_key] = (
                    self.__sensor_rpm / (self.__gear_ratio * 60)
                ) * self.__wheel_to_meters
            else:
                self.__ignore_next = True

    def apply_steering(self, steering):
        """Change steering.

        Args:
            steering (float): steering between -1 and 1.
        """
        self.__steering = int(utils.map_value(steering, -1, 1, 0, 255))
        self.__command[1] = self.__steering
        self.ser.write(self.__command)

    def apply_throttle(self, throttle):
        """Change motor throttle.

        Args:
            throttle (float): throttle between -1 and 1.
        """
        self.__throttle = int(utils.map_value(throttle, -1, 1, 0, 255))
        self.__command[2] = self.__throttle
        self.ser.write(self.__command)

    def apply_steering_throttle(self, steering, throttle):
        """Change all the elements at the same time.

        Args:
            steering (float): steering between -1 and 1.
            throttle (float): throttle between -1 and 1.
        """
        self.__steering = int(utils.map_value(steering, -1, 1, 0, 255))
        self.__throttle = int(utils.map_value(throttle, -1, 1, 0, 255))

        self.__command[1] = self.__steering
        self.__command[2] = self.__throttle
        self.ser.write(self.__command)

    def update(self):
        """Update steering and throttle using memory."""
        steering = self.__memory.get(self.__steering_key, 0)
        throttle = self.__memory.get(self.__throttle_key, 0)
        self.apply_steering_throttle(steering, throttle)

    def get_sensor_last_received(self):
        return self.__last_received
