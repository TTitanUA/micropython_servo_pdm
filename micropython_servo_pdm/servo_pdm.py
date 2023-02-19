from machine import PWM
from .smooth_servo_simple import ServoSmoothBase, SmoothLinear


class ServoPDM:
    def __init__(self, pwm: PWM, min_us=1000, max_us=9000, max_angle=180, min_angle=0, freq=50, invert=False):
        self.pwm = pwm
        self.pwm.freq(freq)
        self._pulse_period_us = (1000 // freq) * 1000
        self._min_us = min_us if min_us > 0 else 0
        self._max_us = max_us if min_us < max_us < self._pulse_period_us else 0
        self._invert = invert
        self._angle_inverse = min_angle > max_angle
        self._angle = min_angle
        self._max_angle = max_angle
        self._min_angle = min_angle
        self._range_angle = abs(max_angle - min_angle) if not self._angle_inverse else abs(min_angle - max_angle)
        self._range_duty = self._max_us - self._min_us

    def __delete__(self, instance):
        self.deinit()

    def set_duty(self, duty_us: int):
        self.pwm.duty_ns(duty_us * 1000)

    def set_angle(self, angle: int):
        angle = self._normalize_angle(angle)
        self._angle = angle
        self.set_duty(self.__get_duty(angle))

    def release(self):
        self._release()

    def deinit(self):
        self.pwm.deinit()

    def _release(self):
        self.set_duty(0)

    def _normalize_angle(self, angle: int):
        if not self._angle_inverse:
            if angle < self._min_angle:
                return self._min_angle
            elif angle > self._max_angle:
                return self._max_angle
        else:
            if angle > self._min_angle:
                return self._min_angle
            elif angle < self._max_angle:
                return self._max_angle
        return angle

    def __get_duty(self, angle: int):
        if not self._angle_inverse:
            percent = abs((angle - self._min_angle) / self._range_angle)
        else:
            percent = abs((self._min_angle - angle) / self._range_angle)

        if self._invert:
            percent = 1 - percent

        return int(self._min_us + (self._range_duty * percent))

    async def _move_gen(self, angle: int, time_ms: int, smooth: type(ServoSmoothBase) = SmoothLinear):
        if smooth is None:
            smooth = SmoothLinear
        angle = self._normalize_angle(angle)

        _curr_duty = self.pwm.duty_ns() // 1000
        _end_duty = self.__get_duty(angle)
        _p_period_ms = self._pulse_period_us // 1000
        self._angle = angle

        if _end_duty > _curr_duty:
            gen = smooth(_end_duty, time_ms, _curr_duty)
            for next_duty in gen.generate(_p_period_ms):
                self.set_duty(next_duty)
                yield _p_period_ms
        else:
            gen = smooth(_curr_duty, time_ms, _end_duty)
            for next_duty in gen.generate(_p_period_ms):
                self.set_duty((_curr_duty - next_duty) + _end_duty)
                yield _p_period_ms
