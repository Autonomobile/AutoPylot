"""
Replay Dataset example,
using the replay camera, it shows a replay of the dataset passed in argument.

usage example: 'python replay_dataset_camera.py C:\\Users\\user\\datasets\\dataset1'
"""

import os
import sys

from autopylot.cameras import camera
from autopylot.utils import logger, memory, vis

# init the logger handlers, select the address to the telemetry server
logger.init(host="localhost", port=8080)

mem = memory.mem


def main(path):
    cam = camera.Camera(camera_type="replay", dataset_path=path)
    while True:
        cam.update()
        vis.show(mem["image"])


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Please provide a path for the data"
    main(os.path.normpath(sys.argv[1]))
