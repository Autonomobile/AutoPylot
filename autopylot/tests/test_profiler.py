import os

from autopylot.utils import profiler


def test_profiler_logs():
    if os.path.exists(profiler.pathlogs):
        os.remove(profiler.pathlogs)

    pr = profiler.Profiler()
    pr.update()

    assert os.path.exists(profiler.pathlogs)


def test_profiler_no_logs():
    if os.path.exists(profiler.pathlogs):
        os.remove(profiler.pathlogs)

    pr = profiler.Profiler(save=False)
    pr.update()

    assert not os.path.exists(profiler.pathlogs)


def test_profiler_n_iter():
    if os.path.exists(profiler.pathlogs):
        os.remove(profiler.pathlogs)

    pr = profiler.Profiler(n_iter=5)
    for i in range(4):
        pr.update()
        assert not os.path.exists(profiler.pathlogs)

    pr.update()
    assert os.path.exists(profiler.pathlogs)
