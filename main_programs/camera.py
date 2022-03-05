import logging

from autopylot.cameras import camera
from autopylot.utils import logger, memory

# init the logger handlers
logger.init()

mem = memory.Memory()
cam = camera.Camera(mem)


def main():
    while True:
        cam.update()  # get the last frame from the camera
        logging.log(logging.TELEMETRY, mem)


if __name__ == "__main__":
    main()
