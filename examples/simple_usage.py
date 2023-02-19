import utime
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
servo = ServoPDM(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle, invert=False)

# set the 30-degree angle
servo.set_angle(120)
utime.sleep(2)

# release the servo
servo.release()
utime.sleep(2)


# manually set the servo duty time
servo.set_duty(min_us + 300)
utime.sleep(1)

# deinit the servo
servo.deinit()
