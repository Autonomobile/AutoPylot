"""File containing the Profiler class used to keep track of the performance of functions."""
import cProfile
import io
import logging
import pstats

from .settings import settings


class Profiler:
    """Profiler class."""

    def __init__(self):
        """Init of the class."""
        self.it = 1

        self.pr = cProfile.Profile()
        self.pr.enable()

        logging.info("Profiler class initialized.")

    def update(
        self,
        filters=settings.PROFILER_FILTERS,
        sort_by=settings.PROFILER_SORT_BY,
        n_iter=settings.PROFILER_N_ITER,
    ):
        """Update of the profiler.

        Args:
            filters (list[str], optional): filters for the profiler results. Defaults to settings.PROFILER_FILTERS.
            sort_by (string, optional): the key to sort the results. Defaults to settings.PROFILER_SORT_BY.
            n_iter (int, optional): positive integer.
            Number of iterations before processing the results. Defaults to settings.PROFILER_N_ITER.
        """
        if self.it % n_iter == 0:
            s = io.StringIO()
            ps = pstats.Stats(self.pr, stream=s).sort_stats(sort_by)
            ps.print_stats(*filters)

            with open(settings.PROFILER_PATH, "w") as f:
                f.write(s.getvalue())

            if settings.PROFILER_RESET:
                self.pr = cProfile.Profile()

            self.it = 1
            self.pr.enable()
        else:
            self.it += 1
