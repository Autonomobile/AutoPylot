"""
Example script for the logging of telemetry.
"""
import logging

from autopylot.cameras import camera
from autopylot.utils import logger, profiler


# init the profiler
pr = profiler.Profiler()

# init the logger handlers, select the address to the telemetry server
logger.init()

cam = camera.Camera(index=0)

# this is a text log
logging.log(logging.DEBUG, "printing !")


def main():
    while True:
        cam.update()  # get the last frame from the camera
        pr.update()


if __name__ == "__main__":
    main()
