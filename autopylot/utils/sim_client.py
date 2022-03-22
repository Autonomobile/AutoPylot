import json
import logging
import time

import numpy as np
from gym_donkeycar.core.sim_client import SDClient

from .settings import settings
from .utils import decode_image


class SimClient(SDClient):
    """Sim Client.

    Args:
        SDClient: basic sim interface client
    """

    def __init__(self, adress=(settings.SIM_HOST, settings.SIM_PORT)):
        super().__init__(*adress, poll_socket_sleep_time=0.005)

        self.image = np.zeros(tuple(settings.IMAGE_SHAPE))
        self.speed = 0
        self.last_received = time.time()

    def on_msg_recv(self, json_packet):
        """Called when a new message is received.

        Args:
            json_packet (dict): json packet.
        """
        try:
            msg_type = json_packet["msg_type"]

            if msg_type == "car_loaded":
                self.car_loaded = True
            elif msg_type == "aborted":
                self.aborted = True
            elif msg_type == "telemetry":
                self.image = decode_image(json_packet["image"])
                self.speed = json_packet["speed"]
                self.last_received = time.time()
            else:
                logging.info(f"received packet with unknowned type: {msg_type}")

        except Exception as msg:
            logging.error(msg)

    def send_controls(self, steering, throttle, brake=0.0):
        """Send control message to the server

        Args:
            steering (float): the steering value.
            throttle (float): the throttle value.
            brake (float, optional): the brake value. Defaults to 0.0.
        """
        p = {
            "msg_type": "control",
            "steering": steering.__str__(),
            "throttle": throttle.__str__(),
            "brake": brake.__str__(),
        }
        self.send_now(json.dumps(p))

    def get_latest_image(self):
        """Wait for a new image to be available.

        Returns:
            np.array: the image.
        """
        while self.image is None:
            time.sleep(self.poll_socket_sleep_sec)
        return self.image


if settings.CAMERA_TYPE == "sim" or settings.CONTROL_TYPE == "sim":
    client = SimClient()
else:
    client = None
