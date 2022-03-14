"""
Load and visualization of a dataset example,
using the load_sorted_dataset_generator, visualize every image one by one.

usage example: 'python load_and_vis_data.py C:\\Users\\user\\datasets\\dataset1'
"""


import os
import sys

from autopylot.datasets import dataset
from autopylot.utils import logger, profiler, vis

# init the logger handlers, select the address to the telemetry server
logger.init()

# init the profiler, logs into logs/profiler.log
pr = profiler.Profiler()


def main(path):
    for image_data in dataset.load_sorted_dataset_generator(path):
        vis_image = vis.vis_all(image_data)

        pr.update()

        vis.cv2.imshow("vis_image", vis_image)
        vis.cv2.waitKey(1)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Please provide a path for the data"
    main(os.path.normpath(sys.argv[1]))
