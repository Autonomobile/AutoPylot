---
title: Controllers
parent: autopylot
---

## Controllers
A controller is needed in order to have a manual "control" of the car, in our case it can be a joystick / keyboard.

### Controller
To simplify the way to instantiate controller classes, we use the method Controller() declared in autopylot.controllers.py. \
It takes in argument the controller type you want to instantiate and returns the instance of that class. If no arguments are provided, the instance will be created according to the CONTROLLER_TYPE from the JSON settings file.

Example:
```json
{
    "CONTROLLER_TYPE": "xbox",
    "SOME_OTHER_SETTINGS": "test"
}
```
```python
from autopylot.controllers import Controller

controller = Controller()
controller.update()
```
Would instantiate the actuator referring to the CONTROLLER_TYPE: "xbox" (XboxOneJoystick).

*Note: this is the only public method available to instantiate actuators (all the following classes are private).*


### XboxOneJoystick
This is the default controller, it can be selected using the CONTROLLER_TYPE: "xbox" option. \
If you want to force the use of the controller without specifying the CONTROLLER_TYPE, you can use the following:
```python
from autopylot.controllers import Controller

controller = Controller(controller_type="xbox")
controller.update()
```
At every `controller.update` call, the steering and throttle along with some other button info will be fetched from the joystick controller and stored into the memory under the "controller" key.


### Keyboard
This actuator is mostly useful when debugging on a computer without the ability to have a joystick.
A main use case would be to drive in the simulator. It can be selected using the CONTROLLER_TYPE: "keyboard" option. \
If you want to force the use of the keyboard controller without specifying the CONTROLLER_TYPE, you can use the following:
```python
from autopylot.controllers import Controller

controller = Controller(controller_type="keyboard")
controller.update()
```
At every `controller.update` call, the steering and throttle along with some other button info will be fetched from the keyboard controller and stored into the memory under the "controller" key.