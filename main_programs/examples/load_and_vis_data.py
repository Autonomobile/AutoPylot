"""
Load and visualization of a dataset example,
using the load_sorted_dataset_generator, visualize every image one by one.

usage example: 'python load_and_vis_data.py C:\\Users\\user\\datasets\\dataset1'
"""


import os
import sys

from autopylot.datasets import dataset
from autopylot.utils import logger, vis

# init the logger handlers, select the address to the telemetry server
logger.init(host="localhost", port=8080)


def main(path):
    for image_data in dataset.load_sorted_dataset_generator(path):
        vis_image = vis.vis_all(image_data)

        vis.cv2.imshow("vis_image", vis_image)
        vis.cv2.waitKey(0)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Please provide a path for the data"
    main(os.path.normpath(sys.argv[1]))
