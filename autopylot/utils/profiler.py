"""
Load and visualization of a dataset example,
using the load_sorted_dataset_generator, visualize every image one by one.

usage example: 'python load_and_vis_data.py C:\\Users\\user\\datasets\\dataset1'
"""

import cProfile
import io
import logging
import os
import pstats

from .settings import settings

pathlogs = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "logs/profiler.log",
)


class Profiler:
    def __init__(self, n_iter=settings.profiler_n_iter, reset=settings.profiler_reset):
        self.n_iter = n_iter
        self.it = 1

        self.reset = reset

        self.pr = cProfile.Profile()
        self.pr.enable()

        logging.info("Profiler class initialized.")

    def update(
        self,
        filters=settings.profiler_filters,
        sort_by=settings.profiler_sort_by,
    ):
        if self.it % self.n_iter == 0:
            s = io.StringIO()
            ps = pstats.Stats(self.pr, stream=s).sort_stats(sort_by)
            ps.print_stats(*filters)

            with open(pathlogs, "w") as f:
                f.write(s.getvalue())

            if self.reset:
                self.pr = cProfile.Profile()

            self.it = 1
            self.pr.enable()
        else:
            self.it += 1
