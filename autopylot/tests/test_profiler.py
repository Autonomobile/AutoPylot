import os

from autopylot.utils import profiler


def test_profiler_logs():
    if os.path.exists(profiler.pathlogs):
        os.remove(profiler.pathlogs)

    pr = profiler.Profiler()
    pr.update(n_iter=1)

    assert os.path.exists(profiler.pathlogs)


def test_profiler_n_iter():
    if os.path.exists(profiler.pathlogs):
        os.remove(profiler.pathlogs)

    pr = profiler.Profiler()
    for i in range(4):
        pr.update(n_iter=5)
        assert not os.path.exists(profiler.pathlogs)

    pr.update(n_iter=5)
    assert os.path.exists(profiler.pathlogs)
