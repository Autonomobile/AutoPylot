"""
Example script for the logging of telemetry.
"""
import logging

from autopylot.cameras import camera
from autopylot.utils import logger, memory, profiler

# init the profiler
pr = profiler.Profiler(n_iter=100)

# init the logger handlers, select the address to the telemetry server
logger.init()

mem = memory.mem
cam = camera.Camera()


# this is a text log
logging.log(logging.DEBUG, "printing !")


def main():
    while True:
        cam.update()  # get the last frame from the camera
        pr.update()

        # this is a telemetry log (only sent to the telemetry server)
        # logging.log(logging.TELEMETRY, mem)


if __name__ == "__main__":
    main()
