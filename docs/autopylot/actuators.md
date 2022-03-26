---
title: Actuators
parent: autopylot
---

## Actuators
An actuator is something that is responsible for the moving of the car. \
In our case, it will refer to "how should we use our steering and throttle output ?".


### Actuator
To simplify the way to instantiate actuator classes, we use the method Actuator() declared in autopylot.actuators.py. \
It takes in argument the actuator type you want to instantiate and returns the instance of that class.
If no arguments are provided, the instance will be created according to the ACTUATOR_TYPE from the JSON settings file.

Example:
```json
{
    "ACTUATOR_TYPE": "serial",
    "SOME_OTHER_SETTINGS": "test"
}
```
```python
from autopylot.actuators import Actuator

actuator = Actuator()
actuator.update()
```
Would instantiate the actuator referring to the ACTUATOR_TYPE: "serial" (SerialActuator).

*Note: this is the only public method available to instantiate actuators (all the following classes are private).*


### SerialActuator
This is the default actuator, it can be selected using the ACTUATOR_TYPE = "serial" option. \
If you want to force the use of the serial actuator without specifying the ACTUATOR_TYPE, you can use the following:
```python
from autopylot.actuators import Actuator

actuator = Actuator(actuator_type="serial")
actuator.update()
```
At every `actuator.update()` call, the steering and throttle output in the memory will be sent to the Arduino, making the car move.


### Actuator
This actuator is useful if we want to control our car in the simulator. It can be selected using the ACTUATOR_TYPE = "sim" option. \
If you want to force the use of the sim actuator without specifying the ACTUATOR_TYPE, you can use the following:
```python
from autopylot.actuators import Actuator

actuator = Actuator(actuator_type="sim")
actuator.update()
```
At every `actuator.update()` call, the steering and throttle output in the memory will be sent to the simulator, making the simulated car move.
