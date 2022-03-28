import os

from autopylot.utils import profiler, settings

settings = settings.settings


def test_profiler_logs():
    if os.path.exists(settings.PROFILER_PATH):
        os.remove(settings.PROFILER_PATH)

    pr = profiler.Profiler()
    pr.update(n_iter=1)

    assert os.path.exists(settings.PROFILER_PATH)


def test_profiler_n_iter():
    if os.path.exists(settings.PROFILER_PATH):
        os.remove(settings.PROFILER_PATH)

    pr = profiler.Profiler()
    for i in range(4):
        pr.update(n_iter=5)
        assert not os.path.exists(settings.PROFILER_PATH)

    pr.update(n_iter=5)
    assert os.path.exists(settings.PROFILER_PATH)
