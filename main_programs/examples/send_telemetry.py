"""
Example script for the logging of telemetry.
"""
import logging

from autopylot.cameras import camera
from autopylot.utils import logger, memory, profiler

# init the profiler
pr = profiler.Profiler(n_iter=100)

# init the logger handlers, select the address to the telemetry server
logger.init(host="http://localhost:8080")

mem = memory.Memory()
cam = camera.Camera(mem)


# this is a text log
logging.log(logging.DEBUG, "printing !")


def main():
    i = 0
    while True:
        cam.update()  # get the last frame from the camera
        pr.update()

        # telemetry 10 times a second
        if i % 1 == 0:
            # this is a telemetry log (only sent to the telemetry server)
            logging.log(logging.TELEMETRY, mem)
            i = 0
        i += 1


if __name__ == "__main__":
    main()
