from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Irq, SmoothLinear
import utime


# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(21))

# create a servo object
servo = ServoPDMRP2Irq(pwm=servo_pwm, min_us=500, max_us=2500, freq=50, max_angle=180)


def main():
    # move to 90 degrees for 2 seconds, by default the servo will use a linear smoothing
    servo.move_to_angle(90, 2000)

    # wait 3 seconds
    utime.sleep(3)

    # move to 20 degrees for 500 ms, using a SmoothLinear smoothing and running a callback when the movement is finished
    servo.move_to_angle(20, 500, SmoothLinear, callback=lambda: print(f"Servo callback"))

    # wait 3 seconds
    utime.sleep(1)


try:
    main()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo.deinit()

