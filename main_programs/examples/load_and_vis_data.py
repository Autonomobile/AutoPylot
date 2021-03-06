"""
Load and visualization of a dataset example,
using the load_sorted_dataset_generator, visualize every image one by one.
"""

from autopylot.datasets import dataset, transform
from autopylot.models import utils
from autopylot.utils import io, logger, profiler, settings, vis

settings = settings.settings

# init the logger handlers, select the address to the telemetry server
logger.init()

# init the profiler, logs into logs/profiler.log
pr = profiler.Profiler()


model, model_info = utils.load_model(
    f"{settings.MODEL_NAME}/{settings.MODEL_NAME}.tflite"
)
settings.ENABLE_TRANSFORM = False
transformer = transform.Transform()


def main(path):
    for path in dataset.sort_paths(dataset.get_every_json_paths(path)):
        image_data = io.load_image_data(path)
        vis_image = vis.vis_all(image_data)
        transformer(image_data)

        predictions = model.predict(image_data)

        predictions["steering"] = (
            predictions["steering.0"] * 1 + predictions["steering.5"] * 1
        ) / 2
        image_data.update(predictions)

        # print(image_data["zone"])

        vis_pred = vis.vis_all(image_data)
        pr.update()

        vis.cv2.imshow("vis_image", vis_image)
        vis.cv2.imshow("vis_pred", vis_pred)
        vis.cv2.waitKey(0)


if __name__ == "__main__":
    main(settings.DATASET_PATH)
