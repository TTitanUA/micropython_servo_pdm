[![pypi version shield](https://img.shields.io/pypi/v/micropython-servo-pdm)](https://pypi.org/project/micropython-servo-pdm/) 
[![pypi downloads per month shield](https://img.shields.io/pypi/dm/micropython-servo-pdm?color=brightgreen)](https://pypi.org/project/micropython-servo-pdm/)
# Servo PDM Continuous
A library for controlling servos through the PWM interface of the Raspberry Pi Pico microcontroller in MicroPython.

Library features:
- Rotate by specified angle
- Smooth change of the angle of rotation
- Cancel hold angle
- Ability to use the [smooth-servo](https://pypi.org/project/smooth-servo/) library to change the smooth start and stop algorithm
- All pending work happens in the background, with two processing options:
     - Using an asyncio task (recommended)
     - Interrupt timer

If you don't need all the functionality listed above, then you should take a look at the [micropython-servo](https://pypi.org/project/micropython-servo/) library.
It is much smaller and better suited for simple tasks.

The following materials were used in the development of the library:
- Material [PDM servos with angle hold](http://wiki.amperka.ru/articles:servo-pdm-standard)), author amperka.ru
- Material [Servo Motor with Raspberry Pi Pico using MicroPython](https://microcontrollerslab.com/servo-motor-raspberry-pi-pico-micropython/) by microcontrollerslab.com
- Material [Hobby Servo Tutorial](https://learn.sparkfun.com/tutorials/hobby-servo-tutorial?_ga=2.2724022.723022425.1676642363-1173110823.1674579241) by MIKEGRUSIN and BYRON J. (sparkfun.com)

### Compatibility
- MicroPython 1.19.1
- Raspberry Pi Pico

On the hardware above the library has been tested and works correctly.

### ATTENTION
You use this module at your own risk.
I am new to MicroPython programming. So there may be nuances that I did not take into account.
If you notice an error or have suggestions for improvement, please write to Issues.

<a name="install"></a>
## Installation
- Install the library via pip (Thonny -> Manage Packages) by name **micropython-servo-pdm**
- Or manual installation:
   - [Download library from GitHub](https://github.com/TTitanUA/micropython_servo_pdm)
   - take the **micropython_servo_pdm** folder from the archive.
   - upload to the root of the microcontroller or to the **lib** folder.

If you want to play around with the logic of the library, then the 2nd installation option is preferable. :)

<a name="init"></a>
## Initialization
### Initializing the base library
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDM

# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(21))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# create a servo object
servo = ServoPDM(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)
```
After that, [basic methods](https://github.com/TTitanUA/micropython_servo_pdm#doc_base) of controlling the servo will be available to you, which do not require pending tasks.

To access additional methods that require deferred execution, you need to initialize one of the child classes.
Depending on which of the ways you prefer to handle pending tasks:

#### Using the uasyncio library
This is the best option for most projects.
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Async

# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(21))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# create a servo object
servo = ServoPDMRP2Async(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)
```

#### Using timer interrupts
You can read more about timers [here](https://docs.micropython.org/en/latest/library/machine.Timer.html)
For Raspberry Pi Pico [here](https://docs.micropython.org/en/latest/rp2/quickref.html#timers)
Be careful, although this is the easiest option, it is not optimal.
Since the handling of servo events occurs in a timer interrupt, other interrupts will be delayed.
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Irq

# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(21))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# create a servo object
servo = ServoPDMRP2Irq(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)
```

<a id="doc"></a>
## Documentation
<a id="doc_pdm"></a>
### A little about PDM
PDM(pulse-duration modulation) is a process of power control by pulsing the power consumer on and off. By Wikipedia®
In our case, it is used to control the servo. By the time of the pulse, you can set the position of the servo shaft.
**ATTENTION:** Unlike PWM, the control is not based on frequency, but on the duration of the pulse.
You can read more here (with pictures): [wiki.amperka.ru](http://wiki.amperka.ru/articles:servo-pdm-standard#%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F)

For the correct operation of the servo, we need to set the following parameters:
- **freq** - pulse frequency, for analog servos 50 Hz. For digital 300 Hz or more.
- **min_us** - minimum pulse time at which the servo goes to the `min_angle` point.
- **max_us** - maximum pulse time at which the servo goes to the `max_angle` point.
- **min_angle** - minimum servo rotation angle.
- **max_angle** - maximum servo rotation angle.
It should be noted that the parameters `min_angle` and `max_angle` set the working area of the servo.
Those. if the servo can rotate from 0 to 180 degrees, then it is not necessary to set `min_angle=0, max_angle=180`,
it could be: `min_angle=-90, max_angle=90`, `min_angle=180, max_angle=0` or so on.


Where can I get these parameters for a specific servo? It all depends on the manufacturer. But in most cases they are specified in the documentation.
But there may also be inaccuracies, for example, there is a drive [MG90S](https://pdf1.alldatasheet.com/datasheet-pdf/view/1132104/ETC2/MG90S.html)
the documentation states that the minimum pulse time is ~1ms, and the maximum is ~2ms.
But in practice it is 0.5ms and 2.5ms (actually 0.35ms and 2.65ms, but these are extreme points outside the operating range of 180 degrees).
So I recommend checking these parameters manually using the `set_duty` method.
How to do manual configuration is in the examples folder the file [manual_config.py](https://github.com/TTitanUA/micropython_servo_pdm/tree/main/examples/manual_config.py) and [encoder_config.py](https://github.com/TTitanUA/micropython_servo_pdm/tree/main/examples/encoder_config.py).

List of parameters for servos:
- **MG90S** - `min_us=500`, `max_us=2500`, `freq=50`, `min_angle=0`, `max_angle=180`
- **SG90** - `min_us=600`, `max_us=2500`, `freq=50`, `min_angle=0`, `max_angle=180`
- **MG995** - `min_us=500`, `max_us=2400`, `freq=50`, `min_angle=0`, `max_angle=180`

**PLEASE:** If you find parameters for a servo that are not listed, submit them to me via [issue](https://github.com/TTitanUA/micropython_servo_pdm/issues).

### ServoPDM constructor parameters
**ServoPDMRP2Async** and **ServoPDMRP2Irq** inherit it and have the same parameters

| Parameter | Type | Default | Description            |
|-----------|------|---------|------------------------|
| pwm       | PWM  | None    | PWM controller         |
| min_us    | int  | 1000    | Minimum pulse time     |
| max_us    | int  | 9000    | Maximum pulse time     |
| min_angle | int  | 0       | Minimum rotation angle |
| max_angle | int  | 180     | Maximum rotation angle |
| freq      | int  | 50      | Pulse frequency        |
| invert    | bool | False   | Direction inversion    |

- `pwm` - [PWM](https://docs.micropython.org/en/latest/library/machine.PWM.html) controller object.
- `min_us` - Minimum pulse time (duty cycle) [More](https://github.com/TTitanUA/micropython_servo_pdm#doc_pdm).
- `max_us` - Maximum pulse time (duty cycle) [More](https://github.com/TTitanUA/micropython_servo_pdm#doc_pdm)
- `min_angle`, `max_angle` - Conditional range of servo operation. You can set any values depending on your tasks and the capabilities of the servo.
- `freq` - Pulse frequency, for analog drives it is 50. Digital drives are usually 300 or more.
- `invert` - Invert the direction of the servo. If `True` then the servo will rotate in the opposite direction.

<a id="doc_base"></a>
### ServoPDM base class methods
- `set_duty(duty_us: int)` - Sets an arbitrary value of the pulse duration in microseconds, from 0 to `(1000 // freq) * 1000`.
This method is intended for manual search of the minimum and maximum duty cycle values. [More](https://github.com/TTitanUA/micropython_servo_pdm#doc_pdm)
- `set_angle(angle: int)` - Sets the angle of the servo, in the range `min_angle < angle < max_angle` (or `max_angle < angle < min_angle` if `min_angle > max_angle`).
- `release()` - Sets the pulse duration to 0, thus disabling position holding by the servo.
- `deinit()` - Disables PWM generation.

### ServoPDMRP2Async and ServoPDMRP2Irq class methods
Well, one method, to be precise :).
- `move_to_angle(...)` - Smoothly moves the servo to the specified angle.

| Parameter       | Type                  | Default      | Description                                                    |
|-----------------|-----------------------|--------------|----------------------------------------------------------------|
| angle           | Int                   | None         | End angle of rotation                                          |
| time_ms         | Int                   | None         | Move time                                                      |
| start_smoothing | type(ServoSmoothBase) | SmoothLinear | Ease class to be used for movement                             |
| callback        | callable              | None         | The function that will be called after the end of the command. |


### Slowdowns
To control slowdowns, you can use the `ServoSmoothBase` classes and its descendants.
This library only has `SmoothLinear` linear deceleration, if you need more, install the [smooth-servo](https://pypi.org/project/smooth-servo/) library.
An example of using built-in easing:
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Async, SmoothLinear

# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(21))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# create a servo object
servo = ServoPDMRP2Async(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)

# Повернуть сервопривод до отметки в 50 градусов за 2 секунды используя линейное замедление. После вывести в консоль "callback cv"
servo.move_to_angle(50, 2000, SmoothLinear, callback=lambda: print("callback move_to_angle"))
```
Details about the parameters and types of slowdowns can be found in the [smooth_servo documentation](https://github.com/TTitanUA/smooth_servo#doc).


## Examples
Usage examples can be found in the [examples](https://github.com/TTitanUA/micropython_servo_pdm/tree/main/examples)  folder.


<a id="feedback"></a>
## Bugs and feedback
If you find bugs, create [issue](https://github.com/TTitanUA/micropython_servo_pdm/issues)
The library is open for further development and your [pull requests](https://github.com/TTitanUA/micropython_servo_pdm/pulls)!
