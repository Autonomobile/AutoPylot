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

    def __init__(self, address=(settings.SIM_HOST, settings.SIM_PORT)):
        super().__init__(*address, poll_socket_sleep_time=0.005)

        self.image = np.zeros(tuple(settings.IMAGE_SHAPE))

        self.last_received = time.time()
        self.speed = 0

        self.node_positions = {}
        self.total_nodes = 0

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
                self.total_nodes = json_packet["totalNodes"]
                self.last_received = time.time()
            elif msg_type == "node_position":
                del json_packet["msg_type"]
                self.node_positions[json_packet["index"]] = json_packet
            else:
                logging.debug(f"received packet with unknowned type: {msg_type}")

        except Exception as msg:
            logging.error(msg)

    def send_controls(self, steering, throttle, brake=0.0):
        """Send control message to the server

        Args:
            steering (float): the steering value.
            throttle (float): the throttle value.
            brake (float, optional): the brake value. Defaults to 0.0.
        """
        msg = {
            "msg_type": "control",
            "steering": steering.__str__(),
            "throttle": throttle.__str__(),
            "brake": brake.__str__(),
        }
        self.send_now(json.dumps(msg))

    def set_position(self, car_pos, car_rot):
        """Force set the position and rotation of the car.

        Args:
            car_pos (np.array): the position of the car.
                (pos_x, pos_y, pos_z)
            car_rot (np.array): the rotation of the car.
                (Qx, Qy, Qz, Qw)
        """
        msg = {"msg_type": "set_position"}
        if len(car_pos) == 3:
            msg["pos_x"] = car_pos[0].__str__()
            msg["pos_y"] = car_pos[1].__str__()
            msg["pos_z"] = car_pos[2].__str__()
        if isinstance(car_rot, np.quaternion):
            msg["Qx"] = car_rot.x.__str__()
            msg["Qy"] = car_rot.y.__str__()
            msg["Qz"] = car_rot.z.__str__()
            msg["Qw"] = car_rot.w.__str__()
        self.send_now(json.dumps(msg))

    def get_node_info(self, index=0):
        """Get the position and rotation of a node

        Args:
            index (int, optional): the index of the node. Defaults to 0.

        Returns:
            dict: the node info.
        """
        msg = {"msg_type": "node_position", "index": str(index)}
        self.send_now(json.dumps(msg))
        while index not in self.node_positions.keys():
            pass
        return self.node_positions[index]

    def get_latest_image(self):
        """Wait for a new image to be available.

        Returns:
            np.array: the image.
        """
        while self.image is None:
            time.sleep(self.poll_socket_sleep_sec)
        img, self.image = self.image, None

        return img


client = SimClient()
