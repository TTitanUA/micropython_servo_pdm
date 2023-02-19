from machine import PWM, Timer
from .smooth_servo_simple import ServoSmoothBase, SmoothLinear
from .servo_pdm import ServoPDM
import uasyncio as asyncio
import utime


class ServoPDMRP2Async(ServoPDM):
    """Wrapper for ServoPDM to add some async functionality to it, based on asyncio"""

    def __init__(self, pwm: PWM, min_us=1000, max_us=9000, max_angle=180, min_angle=0, freq=50, invert=False):
        super().__init__(pwm, min_us, max_us, max_angle, min_angle, freq, invert)
        self._task = None

    def move_to_angle(self, angle: int, time_ms: int, smooth: type(ServoSmoothBase) = SmoothLinear, callback: callable = None):
        if self._task is not None and not self._task.done():
            self._task.cancel()

        try:
            self._task = asyncio.create_task(
                self._move_task(
                    self._move_gen(angle, time_ms, smooth),
                    callback
                )
            )
        except asyncio.CancelledError:
            pass

    def release(self):
        if self._task is not None and not self._task.done():
            self._task.cancel()

        self._release()

    async def _move_task(self, generator, callback: callable = None):
        for sleep in generator:
            await asyncio.sleep_ms(sleep)

        self.__call_callback(callback)
        self._task = None

    def _release(self):
        super()._release()

    @staticmethod
    def __call_callback(callback: callable = None):
        if callback is not None and callable(callback):
            try:
                callback()
            except Exception as e:
                print('ServoPDMRP2Async error in callback', e)

    @staticmethod
    def __normalize_time(time):
        if time < 0:
            return 0
        return int(time)


class ServoPDMRP2Irq(ServoPDM):
    """Wrapper for ServoPDM to add some async functionality to it, based on irq timer"""

    def __init__(self, pwm: PWM, min_us=1000, max_us=9000, max_angle=180, min_angle=0, freq=50, invert=False):
        super().__init__(pwm, min_us, max_us, max_angle, min_angle, freq, invert)
        self._continue_action_at = 0
        self._last_action_generator = None
        self.__tick_execution_time = self._pulse_period_us // 1000
        self._timer = Timer(-1, mode=Timer.PERIODIC, period=self._pulse_period_us // 1000, callback=self.__timer_tick)
        self.__last_callback = None

    def move_to_angle(self, angle: int, time_ms: int, smooth: type(ServoSmoothBase) = SmoothLinear, callback: callable = None):
        self.__last_callback = callback
        self.__move_generator(self._move_gen(angle, time_ms, smooth))

    def release(self):
        self._release()

    def _release(self):
        self._continue_action_at = 0
        self._last_action_generator = None
        super()._release()

    def __move_generator(self, generator):
        self._last_action_generator = generator
        try:
            self._continue_action_at = next(self._last_action_generator) + utime.ticks_ms()
        except StopIteration:
            self._last_action_generator = None
            self.__call_callback()
        except Exception as e:
            print('ServoPDMRP2Irq error in __run_generator', e)
            self.release()

    def __call_callback(self):
        if self.__last_callback is not None and callable(self.__last_callback):
            _callback = self.__last_callback
            self.__last_callback = None
            try:
                _callback()
            except Exception as e:
                print('ServoPDMRP2Irq error in callback', e)

    def __timer_tick(self, *args):
        try:
            if self._last_action_generator is not None:
                next(self._last_action_generator)
        except ValueError:
            pass
        except StopIteration:
            self._last_action_generator = None
            self.__call_callback()
        except Exception as e:
            print('ServoPDMRP2Irq error in timer tick', e, type(e))
            self.release()
