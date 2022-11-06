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
settings.ENABLE_TRANSFORM = True
transformer = transform.Transform()


def main(path):
    for path in dataset.sort_paths(dataset.get_every_json_paths(path)):
        image_data = io.load_image_data(path)
        transformer(image_data)
        vis_image = vis.vis_all(image_data)

        predictions = model.predict(image_data)
        image_data.update(predictions)

        image_data["steering"] = image_data["steering.0"]

        vis_pred = vis.vis_all(image_data)
        pr.update()

        vis.cv2.imshow("vis_image", vis_image)
        vis.cv2.imshow("vis_pred", vis_pred)
        vis.cv2.waitKey(0)


if __name__ == "__main__":
    main(settings.DATASET_PATH)
