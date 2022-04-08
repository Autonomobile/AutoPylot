import cv2
import numpy as np

from ..utils import settings

settings = settings.settings


def _brightness(image_data):
    value = np.random.randint(15, 45)
    sign = np.random.choice([True, False])
    hsv = cv2.cvtColor(image_data["image"], cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    if sign:
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] = v[v <= lim] + value
    if sign:
        lim = 0 + value
        v[v < lim] = 0
        v[v >= lim] = v[v >= lim] - value

    hsv = cv2.merge((h, s, v))
    image_data["image"] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def _shadow(image_data):
    top_y = settings.IMAGE_SHAPE[1] * np.random.uniform()
    top_x = settings.IMAGE_SHAPE[0] * np.random.uniform()
    bot_x = settings.IMAGE_SHAPE[0] * np.random.uniform()
    bot_y = settings.IMAGE_SHAPE[1] * np.random.uniform()

    image_hls = np.array(
        cv2.cvtColor(image_data["image"], cv2.COLOR_BGR2HLS), dtype=np.uint16
    )
    shadow_mask = 0 * image_hls[:, :, 1]

    X_m = np.mgrid[0 : settings.IMAGE_SHAPE[0], 0 : settings.IMAGE_SHAPE[1]][0]
    Y_m = np.mgrid[0 : settings.IMAGE_SHAPE[0], 0 : settings.IMAGE_SHAPE[1]][1]

    shadow_mask[
        ((X_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (Y_m - top_y) >= 0)
    ] = 1

    sign = np.random.choice([True, False])
    if sign:
        random_bright = 1 + 0.3 * np.random.uniform()
    else:
        random_bright = 1 - 0.3 * np.random.uniform()

    cond1 = shadow_mask == 1
    cond0 = shadow_mask == 0

    if np.random.randint(2) == 1:
        image_hls[:, :, 1][cond1] = image_hls[:, :, 1][cond1] * random_bright
    else:
        image_hls[:, :, 1][cond0] = image_hls[:, :, 1][cond0] * random_bright

    image_hls[image_hls[:, :, 1] >= 255] = 255
    image_hls = np.array(image_hls, dtype=np.uint8)
    image_data["image"] = cv2.cvtColor(image_hls, cv2.COLOR_HLS2BGR)


def _blur(image_data):
    image_data["image"] = cv2.blur(image_data["image"], (2, 2))


def _flip(image_data):
    image_data["image"] = cv2.flip(image_data["image"], 1)
    image_data["steering"] *= -1


def _noise(image_data):
    image_data["image"] += np.random.uniform(-25, 25, size=settings.IMAGE_SHAPE)


class Augmentation:
    def __init__(self, frequency, do_flip=True):
        self.frequency = frequency
        self.do_flip = do_flip
        self.functions = [_brightness, _shadow, _blur, _noise]

    def __call__(self, image_data):
        if self.do_flip and np.random.uniform() < 0.5:
            _flip(image_data)

        for func in self.functions:
            try:
                if np.random.uniform() < self.frequency:
                    func(image_data)
            except Exception:
                pass
