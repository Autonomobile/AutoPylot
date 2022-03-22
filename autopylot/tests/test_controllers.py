from ..controllers import Controller
from ..utils import memory
from ..cameras import camera


def test_joystick_not_init():
    """Test the controller dict when joystick is not connected."""
    mem = memory.mem
    cam = camera.Camera(mem, camera_type="dummy")
    cam.update()

    js = Controller(mem, controller_type="xbox")
    js.update()

    # no controls as controller is not init
    assert len(mem) == 2 and mem["controller"] == {}
