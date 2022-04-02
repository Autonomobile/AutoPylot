from ..controllers import Controller
from ..utils import memory
from ..cameras import camera


def test_joystick_not_init():
    """Test the controller dict when joystick is not connected."""
    mem = memory.mem
    cam = camera.Camera(mem, camera_type="dummy")
    cam.update()

    controller = Controller(mem, controller_type="xbox", do_init=False)
    controller.update()

    # no controls as controller is not init
    assert len(mem) == 2 and mem["controller"] == {}
