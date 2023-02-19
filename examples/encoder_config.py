import uasyncio as asyncio
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDM

# This is an example of finding pulse time settings for your servo on raspberry pi pico using encoder.
# Connect the servo signal wire to GPIO21 on the Pico.
# Connect encoder contacts: clk - GPIO15, dt - GPIO9
# Connect pico to your computer via USB.
# Open the serial monitor in Thonny IDE.
# Create a new file and paste the code from this file to it.
# Set `freq` to the frequency of your servo.
# Run the code.
# LRotate the encoder and note down the values when the servo starts moving and when it stops.
# These will be the extreme points of the servo, I recommend stepping back from them by 100-200 milliseconds.
# Example: servo starts moving at 350 microseconds, stops moving at 2700 microseconds. Set `min_us` to 500 and `max_us` to 2500.
# This will give a small margin for the working stroke of the drive and reduce the likelihood of the mechanism jamming at extreme points.
# You can change the `iteration_time_ms` to make the process faster or slower.
# By changing the values of `min_us`, `max_us` and `step_us` you can limit the search area and change the search step.



# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(21))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 0
max_us = (1000 // freq) * 1000
iteration_time_ms = 500
step_us = 50
duty = 0

# create a servo object
servo = ServoPDM(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq)


# Create the encoder object
en_pin_clk = Pin(15, Pin.IN, Pin.PULL_UP)
en_pin_dt = Pin(9, Pin.IN, Pin.PULL_UP)

# Create the rotary encoder object
encoder = RotaryEncoderRP2(
    pin_clk=en_pin_clk,
    pin_dt=en_pin_dt,
)


def turn_left_listener(fast: bool = False):
    global duty
    duty -= step_us if not fast else step_us * 10
    print(f"duty: {duty}")
    servo.set_duty(duty)


def turn_right_listener(fast: bool = False):
    global duty
    duty += step_us if not fast else step_us * 10
    print(f"duty: {duty}")
    servo.set_duty(duty)


encoder.on(RotaryEncoderEvent.TURN_LEFT, lambda: turn_left_listener())
encoder.on(RotaryEncoderEvent.TURN_LEFT_FAST, lambda: turn_left_listener(True))

encoder.on(RotaryEncoderEvent.TURN_RIGHT, lambda: turn_right_listener())
encoder.on(RotaryEncoderEvent.TURN_RIGHT_FAST, lambda: turn_right_listener(True))


try:
    print("Turn the encoder to set the duty cycle of the servo.")
    asyncio.run(encoder.async_tick())
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo.deinit()

