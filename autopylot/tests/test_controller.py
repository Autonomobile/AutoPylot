from ..controls import controller
from ..utils import memory
from ..cameras import camera


def test_controller():
    """Test the controller dict when joystick is not connected."""
    mem = memory.mem
    cam = camera.Camera(mem, camera_type="dummy")
    cam.update()

    js = controller.XboxOneJoystick(mem)
    js.update()

    # no controls as controller is not init
    assert len(mem) == 2 and mem["controller"] == {}
