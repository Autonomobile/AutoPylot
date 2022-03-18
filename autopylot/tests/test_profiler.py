import os

from autopylot.utils import profiler


def test_profiler_logs():
    if os.path.exists(profiler.pathlogs):
        os.remove(profiler.pathlogs)

    pr = profiler.Profiler(n_iter=1)
    pr.update()

    assert os.path.exists(profiler.pathlogs)


def test_PROFILER_N_ITER():
    if os.path.exists(profiler.pathlogs):
        os.remove(profiler.pathlogs)

    pr = profiler.Profiler(n_iter=5)
    for i in range(4):
        pr.update()
        assert not os.path.exists(profiler.pathlogs)

    pr.update()
    assert os.path.exists(profiler.pathlogs)
