import os
import time

import numpy as np
import quaternion
from autopylot.utils import io, settings, sim_client

settings = settings.settings


def get_steering(car_pos, car_rot, target_node_pos, target_node_rot):
    relative_pos = target_node_pos - car_pos
    distance = np.linalg.norm(relative_pos)
    no_rot_relative_pos = (
        quaternion.rotate_vectors(1 / car_rot, relative_pos) / distance
    )

    x_difference = no_rot_relative_pos[0]

    steering = np.clip(x_difference * 1.0, -1.0, 1.0)
    return steering


def generate_data(
    self=sim_client.client,
    track_name="roboracingleague_1",
    collect_path=settings.COLLECT_PATH,
    look_ahead=10,
    height_offset=0.1,
    n_lat=2,
    n_rot_y=3,
    road_width=1.5,
    max_rot=0.15,
):
    """Generate data from a sim track.

    Args:
        self (sim_client.SimClient, optional): the client instance. Defaults to sim_client.client.
        track_name (str, optional): name of the track to load. Defaults to "roboracingleague_1".
        look_ahead (int, optional): number of nodes to look ahead. Defaults to 5.
        height_offset (float, optional): height offset to set the car position. Defaults to 0.
        n_lat (int, optional): number of additionnal lateral positions. Defaults to 2 (4 + 1 in total).
        n_rot_y (int, optional): number of rotations per lateral position. Defaults to 3.
        road_width (int, optional): distance between leftmost and rightmost lateral positions. Defaults to 2.
        max_rot (float, optional): angle in radians of the maximum rotation. Defaults to 0.15.
    """

    collect_path = os.path.join(collect_path, track_name)
    if not os.path.exists(collect_path):
        os.mkdir(collect_path)

    pos_offset_values = [(i / n_lat) * road_width for i in range(-n_lat, n_lat + 1)]
    rot_offset_values = [(i / n_rot_y) * max_rot for i in range(-n_rot_y, n_rot_y + 1)]

    while self.total_nodes == 0:
        time.sleep(self.poll_socket_sleep_sec)

    for i in range(self.total_nodes):
        # fetch all the nodes info
        self.get_node_info(i)

    i = 0
    while i < self.total_nodes:
        node_info = self.get_node_info(i)

        node_pos = np.array(
            [
                node_info["pos_x"],
                node_info["pos_y"] + height_offset,
                node_info["pos_z"],
            ]
        )

        node_rot = np.quaternion(
            node_info["Qx"],
            node_info["Qy"],
            node_info["Qz"],
            node_info["Qw"],
        )

        node_info = self.get_node_info((i + look_ahead) % self.total_nodes)

        target_node_pos = np.array(
            [
                node_info["pos_x"],
                node_info["pos_y"] + height_offset,
                node_info["pos_z"],
            ]
        )

        target_node_rot = np.quaternion(
            node_info["Qx"],
            node_info["Qy"],
            node_info["Qz"],
            node_info["Qw"],
        )

        for pos_x_offset in pos_offset_values:
            offset_pos = np.array([pos_x_offset, 0.0, 0.0])
            offset_pos = quaternion.rotate_vectors(node_rot, offset_pos)
            car_pos = node_pos + offset_pos

            for rot_y_offset in rot_offset_values:
                rot_y_offset_quaternion = np.quaternion(0, rot_y_offset, 0, 1)
                car_rot = node_rot * rot_y_offset_quaternion

                # update the position and rotation of the car
                self.set_position(car_pos, car_rot)

                # make sure to fetch a recent image
                self.get_latest_image()
                image = self.get_latest_image()
                steering = get_steering(
                    car_pos,
                    car_rot,
                    target_node_pos,
                    target_node_rot,
                )
                image_data = {"image": image, "steering": steering}

                io.save_image_data(
                    image_data,
                    os.path.join(
                        collect_path,
                        settings.JSON_FILE_FORMAT.format(t=time.time()),
                    ),
                )

        i += 10


if __name__ == "__main__":
    generate_data()
