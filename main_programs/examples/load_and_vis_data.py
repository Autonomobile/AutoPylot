"""
Load and visualization of a dataset example,
using the load_sorted_dataset_generator, visualize every image one by one.

usage example: 'python load_and_vis_data.py C:\\Users\\user\\datasets\\dataset1'
"""


import os
import sys

from autopylot.datasets import transform, dataset, preparedata
from autopylot.utils import logger, profiler, settings, utils, vis

# init the logger handlers, select the address to the telemetry server
logger.init()

# init the profiler, logs into logs/profiler.log
pr = profiler.Profiler()


model, model_info = utils.load_model(
    f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
)
prepare_data = preparedata.PrepareData(model_info)
transformer = transform.Transform()


def main(path):
    for image_data in dataset.load_sorted_dataset_generator(path):
        transformer(image_data)
        vis_image = vis.vis_all(image_data)

        pr.update()

        vis.cv2.imshow("augm", image_data["image"])
        vis.cv2.imshow("vis_image", vis_image)
        vis.cv2.waitKey(0)


if __name__ == "__main__":
    main(settings.DATASET_PATH)
