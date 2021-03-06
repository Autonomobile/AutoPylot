import cv2
import numpy as np

from ..utils import settings

settings = settings.settings


def get_function_by_name(name):
    """Get the function by name.

    Args:
        name (str): the name of the function.

    Returns:
        function: the function.
    """
    return getattr(Functions, name)


class Functions:
    def brightness(image_data):
        if "image" not in image_data.keys():
            return

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

    def shadow(image_data):
        if "image" not in image_data.keys():
            return

        shape = image_data["image"].shape
        top_y = shape[1] * np.random.uniform()
        top_x = shape[0] * np.random.uniform()
        bot_x = shape[0] * np.random.uniform()
        bot_y = shape[1] * np.random.uniform()

        image_hls = np.array(
            cv2.cvtColor(image_data["image"], cv2.COLOR_BGR2HLS),
            dtype=np.uint16,
        )
        shadow_mask = 0 * image_hls[:, :, 1]

        X_m = np.mgrid[0 : shape[0], 0 : shape[1]][0]
        Y_m = np.mgrid[0 : shape[0], 0 : shape[1]][1]

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

    def saturation(image_data):
        if "image" not in image_data.keys():
            return

        image_hls = np.array(
            cv2.cvtColor(image_data["image"], cv2.COLOR_BGR2HLS), dtype=np.uint16
        )
        image_hls[:, :, 1] = image_hls[:, :, 1] * (1 + 0.3 * np.random.uniform())
        image_hls[image_hls[:, :, 1] >= 255] = 255
        image_hls = np.array(image_hls, dtype=np.uint8)
        image_data["image"] = cv2.cvtColor(image_hls, cv2.COLOR_HLS2BGR)

    def blur(image_data):
        if "image" not in image_data.keys():
            return

        image_data["image"] = cv2.blur(image_data["image"], (2, 2))

    def bilateral_filter(image_data):
        if "image" not in image_data.keys():
            return

        image_data["image"] = cv2.bilateralFilter(image_data["image"], 9, 75, 75)

    def flip(image_data):
        if "image" in image_data.keys():
            image_data["image"] = cv2.flip(image_data["image"], 1)
        image_data["steering"] = image_data["steering"] * -1.0

        if "trajectory" in image_data.keys():
            for i in range(len(image_data["trajectory"]) // 2):
                image_data["trajectory"][i * 2] *= -1.0

    def noise(image_data):
        if "image" not in image_data.keys():
            return

        image_data["image"] = (
            image_data["image"] + np.random.randint(-25, 25, size=settings.IMAGE_SHAPE)
        ).astype(np.uint8)

    def shift(image_data):
        if "image" in image_data.keys():
            x_offset = np.random.randint(-20, 20)
            y_offset = np.random.randint(-5, 5)
            M = np.float32([[1, 0, x_offset], [0, 1, y_offset]])

            image_data["image"] = cv2.warpAffine(
                image_data["image"],
                M,
                (settings.IMAGE_SHAPE[1], settings.IMAGE_SHAPE[0]),
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(127, 127, 127),
            )

        image_data["steering"] += (x_offset * 2) / settings.IMAGE_SHAPE[0]

    def grayscale(image_data):
        if "image" not in image_data.keys():
            return

        image_data["image"] = cv2.cvtColor(image_data["image"], cv2.COLOR_BGR2GRAY)
        image_data["image"] = cv2.cvtColor(image_data["image"], cv2.COLOR_GRAY2BGR)

    def mix_channel(image_data):
        if "image" not in image_data.keys():
            return

        img = image_data["image"]
        order = np.split(img, 3, axis=-1)
        np.random.shuffle(order)
        image_data["image"] = cv2.merge(order)

    def resize(image_data):
        if "image" not in image_data.keys():
            return

        factor = 1.0 + image_data.get("batch-random", np.random.uniform(0.0, 1.0))
        shape = image_data["image"].shape
        image_data["image"] = cv2.resize(
            image_data["image"],
            (int(shape[1] * factor), int(shape[0] * factor)),
        )


class Transform:
    def __init__(self, additionnal_funcs=[]):
        """Init the transformation function class.

        Args:
            additionnal_funcs (list(tuple(method, float)), optional): tuple containing the function and the frequency.
        """
        self.functions = [
            (get_function_by_name(name), freq)
            for name, freq in settings.TRANSFORM_FUNCTIONS.items()
            if settings.ENABLE_TRANSFORM
        ] + additionnal_funcs

    def __call__(self, image_data, rands=None):
        if rands is None:
            new_rands = []

        for i, (func, freq) in enumerate(self.functions):
            try:
                if rands is None:
                    rand = np.random.uniform()
                    if rand < freq:
                        func(image_data)
                    new_rands.append(rand)
                else:
                    rand = rands[i]
                    if rand < freq:
                        func(image_data)
            except Exception as e:
                print(image_data, func, freq)
                pass

        if rands is None:
            return new_rands
        else:
            return rands
