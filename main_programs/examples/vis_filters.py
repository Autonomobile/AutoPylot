"""
Load and visualization of a dataset example,
using the load_sorted_dataset_generator, visualize every image one by one.
"""

import numpy as np
import cv2
from autopylot.datasets import dataset, preparedata, transform
from autopylot.models import utils
from autopylot.utils import io, settings, vis


def image_processing(image_data):
    image = image_data["image"]

    image = cv2.bilateralFilter(image, 9, 75, 75)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(image, 100, 150)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    image_data["image"] = image


settings = settings.settings
transformer = transform.Transform(additionnal_funcs=[(image_processing, 1)])


def main(path):
    run = True
    while run:
        for path in dataset.sort_paths(dataset.get_every_json_paths(path)):

            image_data = io.load_image_data(path)

            original_image = image_data["image"].copy()

            transformer(image_data)

            cv2.imshow("init", original_image)
            cv2.imshow("augm", image_data["image"])

            # play image in loop until key is pressed with 60 fps
            # if key q is pressed, stop the loop
            key = cv2.waitKey(1000 // 60)
            if key == ord("q"):
                run = False
                break


if __name__ == "__main__":
    main(settings.DATASET_PATH)
