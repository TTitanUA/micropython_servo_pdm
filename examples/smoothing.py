from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Async
from smooth_servo import SmoothLinear, SmoothEaseIn, SmoothEaseOut, SmoothEaseInQuad, \
    SmoothEaseOutQuad, SmoothEaseInOutQuad, SmoothEaseInCubic, SmoothEaseOutCubic, SmoothEaseInOutCubic, \
    SmoothEaseInQuart, SmoothEaseOutQuart, SmoothEaseInOutQuart, SmoothEaseInQuint, SmoothEaseOutQuint, \
    SmoothEaseInOutQuint, SmoothEaseInExpo, SmoothEaseOutExpo, SmoothEaseInOutExpo, SmoothEaseInCirc, \
    SmoothEaseOutCirc, SmoothEaseInOutCirc, SmoothEaseInBack, SmoothEaseOutBack, SmoothEaseInOutBack, SmoothEaseInOut
import uasyncio as asyncio

# It is possible to use the following smooth variations:
smooth_variations = [
    SmoothLinear,
    SmoothEaseIn,
    SmoothEaseOut,
    SmoothEaseInOut,
    SmoothEaseInQuad,
    SmoothEaseOutQuad,
    SmoothEaseInOutQuad,
    SmoothEaseInCubic,
    SmoothEaseOutCubic,
    SmoothEaseInOutCubic,
    SmoothEaseInQuart,
    SmoothEaseOutQuart,
    SmoothEaseInOutQuart,
    SmoothEaseInQuint,
    SmoothEaseOutQuint,
    SmoothEaseInOutQuint,
    SmoothEaseInExpo,
    SmoothEaseOutExpo,
    SmoothEaseInOutExpo,
    SmoothEaseInCirc,
    SmoothEaseOutCirc,
    SmoothEaseInOutCirc,
    SmoothEaseInBack,
    SmoothEaseOutBack,
    SmoothEaseInOutBack,
]

servo_pwm = PWM(Pin(21))
# Current configuration is for a TowerPro SG90 servo
servo = ServoPDMRP2Async(pwm=servo_pwm, min_us=500, max_us=2500, freq=50, max_angle=180, min_angle=0, invert=False)
duration = 2000
angle = 0
sleep = 1000


async def smooth_test():
    global angle
    for smooth in smooth_variations:
        angle = 180 if angle == 0 else 0
        print(
            f"Smooth: {smooth.__name__}, angle: {angle}, duration: {duration}, sleep: {sleep}")
        servo.move_to_angle(angle, duration, smooth)

        await asyncio.sleep_ms(duration + sleep)
        print("")


try:
    asyncio.run(smooth_test())
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo.stop()

