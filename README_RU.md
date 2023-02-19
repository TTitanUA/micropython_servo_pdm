[![pypi version shield](https://img.shields.io/pypi/v/micropython-servo-pdm)](https://pypi.org/project/micropython-servo-pdm/) 
[![pypi downloads per month shield](https://img.shields.io/pypi/dm/micropython-servo-pdm?color=brightgreen)](https://pypi.org/project/micropython-servo-pdm/)
# Servo PDM Continuous
Библиотека для управления сервоприводами через интерфейс PWM микроконтроллера Raspberry Pi Pico на языке MicroPython.

Возможности библиотеки:
- Поворот на указанный угол
- Плавное изменение угла поворота
- Отмена удержания угла поворота
- Возможность использования библиотеки [smooth-servo](https://pypi.org/project/smooth-servo/) для изменения алгоритма плавного старта и остановки
- Вся отложенная работа происходит в фоновом режиме, с двумя вариантами обработки:
    - С помощью задачи asyncio (рекомендуется)
    - Таймером прерывания

Если вам не нужен весь перечисленный выше функционал, то вам стоит глянуть на библиотеку [micropython-servo](https://pypi.org/project/micropython-servo/).
Она гораздо меньше и для простых задач подходит лучше.

При разработке библиотеки использовались следующие материалы:
- Материал [Сервоприводы PDM с удержанием угла](http://wiki.amperka.ru/articles:servo-pdm-standard), автор amperka.ru
- Материал [Servo Motor with Raspberry Pi Pico using MicroPython](https://microcontrollerslab.com/servo-motor-raspberry-pi-pico-micropython/), автор microcontrollerslab.com
- Материал [Hobby Servo Tutorial](https://learn.sparkfun.com/tutorials/hobby-servo-tutorial?_ga=2.2724022.723022425.1676642363-1173110823.1674579241), автор MIKEGRUSIN and BYRON J. (sparkfun.com)

### Совместимость
- MicroPython 1.19.1
- Raspberry Pi Pico

На представленном выше оборудовании библиотека была протестирована и работает корректно.
Но с не большими костылями она может работать и на другом оборудовании.

### ВНИМАНИЕ
Вы используете данный модуль на свой страх и риск. 
Я новичок в программировании на MicroPython. Так что могут быть нюансы, которые я не учел.
Если вы заметили ошибку или у вас есть предложения по улучшению, то пишите в Issues.

## Содержание
- [Установка](https://github.com/TTitanUA/micropython_servo_pdm#install)
- [Инициализация](https://github.com/TTitanUA/micropython_servo_pdm#init)
- [Документация](https://github.com/TTitanUA/micropython_servo_pdm#doc)
- [Примеры](https://github.com/TTitanUA/micropython_servo_pdm/tree/main/examples)
- [Баги и обратная связь](https://github.com/TTitanUA/micropython_servo_pdm#feedback)

<a id="install"></a>
## Установка
- Библиотеку установить через pip (Thonny -> Manage Packages) по названию **micropython-servo-pdm** 
- Или ручная установка:
  - [Скачать библиотеку с GitHub](https://github.com/TTitanUA/micropython_servo_pdm) 
  - забрать папку **micropython_servo_pdm_continuous** из архива.
  - загрузить в корень микроконтроллера или в папку **lib**.

Если хотите поиграться с логикой библиотеки, то 2й вариант установки предпочтительнее. :)

<a id="init"></a>
## Инициализация
### Инициализация базовой библиотеки
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDM

# создаем PWM контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# создаем объект сервопривода
servo = ServoPDM(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)
```
После этого вам будут доступны [базовые методы](https://github.com/TTitanUA/micropython_servo_pdm#doc_base) управления сервоприводом, которые не требуют отложенных задач.

Для доступа к дополнительным методам, которые требуют отложенного выполнения, вам нужно инициализировать один из дочерних классов. 
В зависимости от того какой из способов обработки отложенных задач вы предпочитаете:

#### С помощью библиотеки uasyncio
Это оптимальный вариант для большинства проектов.
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Async

# создаем PWM контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# создаем объект сервопривода
servo = ServoPDMRP2Async(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)
```

#### С помощью прерываний по таймеру
Подробнее про таймеры можно почитать [здесь](https://docs.micropython.org/en/latest/library/machine.Timer.html)
Для Raspberry Pi Pico [здесь](https://docs.micropython.org/en/latest/rp2/quickref.html#timers)
Будьте внимательны, хоть это и самый простой вариант, но он не оптимален.
Так как обработка событий сервопривода происходит в прерывании по таймеру, другие прерывания будут отложены.
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Irq

# создаем PWM контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# создаем объект сервопривода
servo = ServoPDMRP2Irq(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)
```

<a id="doc"></a>
## Документация
<a id="doc_pdm"></a>
### Немного о PDM
PDM(pulse-duration modulation) - это процесс управления мощностью методом пульсирующего включения и выключения потребителя энергии. By Wikipedia®
В нашем случае она используется для управления сервоприводом. По времени импульса можно задать положение вала сервопривода.
**ВНИМАНИЕ:** В отличие от PWM, управление происходит не по частоте, а по длительности импульса. 
Подробнее можно прочитать тут (с картинками): [wiki.amperka.ru](http://wiki.amperka.ru/articles:servo-pdm-standard#%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F)

Для корректной работы сервопривода, нам необходимо задать следующие параметры:
- **freq** - частота импульсов, для аналоговых сервоприводов 50 Гц. Для цифровых 300 Гц и более.
- **min_us** - минимальное время импульса, при котором сервопривод переходит в точку `min_angle`.
- **max_us** - максимальное время импульса, при котором сервопривод переходит в точку `max_angle`.
- **min_angle** - минимальный угол поворота сервопривода.
- **max_angle** - максимальный угол поворота сервопривода.
Надо отметить, что параметры `min_angle` и `max_angle` задают рабочую область работы сервопривода.
Т.е. если сервопривод может вращаться от 0 до 180 градусов, то необязательно задавать `min_angle=0, max_angle=180`,
это может быть: `min_angle=-90, max_angle=90`, `min_angle=180, max_angle=0` или т.д..


Где взять эти параметры для конкретного сервопривода? Все зависит от производителя. Но в большинстве случаев они указаны в документации.
Но там тоже могут быть не точности, на пример есть привод [MG90S](https://pdf1.alldatasheet.com/datasheet-pdf/view/1132104/ETC2/MG90S.html)
в документации указано, что минимальное время импульса ~1мс, а максимальное ~2мс. 
Но на практике это 0.5мс и 2.5мс (на самом деле 0.35мс и 2.65мс, но это крайние точки за пределами рабочего диапазона в 180 градусов).
Так что я рекомендую проверять эти параметры вручную, используя метод `set_duty`.
Как делать ручную настройку есть в папке примеров файл [manual_config.py](https://github.com/TTitanUA/micropython_servo_pdm/tree/main/examples/manual_config.py) и [encoder_config.py](https://github.com/TTitanUA/micropython_servo_pdm/tree/main/examples/encoder_config.py).


Список параметров для сервоприводов:
- **MG90S** - `min_us=500`, `max_us=2500`, `freq=50`, `min_angle=0`, `max_angle=180`
- **SG90** - `min_us=600`, `max_us=2500`, `freq=50`, `min_angle=0`, `max_angle=180`
- **MG995** - `min_us=500`, `max_us=2400`, `freq=50`, `min_angle=0`, `max_angle=180`

**ПРОСЬБА:** Если вы нашли параметры для сервопривода, которых нет в списке, пожалуйста отправьте мне их через [issue](https://github.com/TTitanUA/micropython_servo_pdm/issues).

### Параметры конструктора ServoPDM
**ServoPDMRP2Async** и **ServoPDMRP2Irq** его наследуют и имеют те же параметры

| Параметр    | Тип  | По умолчанию | Описание                    |
|-------------|------|--------------|-----------------------------|
| pwm         | PWM  | None         | PWM контроллер              |
| min_us      | int  | 1000         | Минимальное время импульса  |
| max_us      | int  | 9000         | Максимальное время импульса |
| min_angle   | int  | 0            | Минимальный угол поворота   |
| max_angle   | int  | 180          | Максимальный угол поворота  |
| freq        | int  | 50           | Частота импульсов           |
| invert      | bool | False        | Инверсия направления        |

- `pwm` - объект [PWM](https://docs.micropython.org/en/latest/library/machine.PWM.html) контроллера.
- `min_us` - Минимальное время импульса (скважность) [Подробнее](https://github.com/TTitanUA/micropython_servo_pdm#doc_pdm).
- `max_us` - Максимальное время импульса (скважность) [Подробнее](https://github.com/TTitanUA/micropython_servo_pdm#doc_pdm)
- `min_angle`, `max_angle` - Условный диапазон работы сервопривода. Вы можете задавать любые значения в зависимости от ваших задач и возможностей сервопривода.
- `freq` - Частота импульсов, для аналоговых приводов это 50. Цифровые обычно 300 и более.
- `invert` - Инверсия направления работы сервопривода. Если `True` то сервопривод будет вращаться в обратную сторону.

<a id="doc_base"></a>
### Методы базового класса ServoPDM
- `set_duty(duty_us: int)` - Устанавливает произвольное значение длительности импульса в микросекундах, от 0 до `(1000 // freq) * 1000`.
Данный метод предназначен для ручного поиска минимального и максимального значения скважности. [Подробнее](https://github.com/TTitanUA/micropython_servo_pdm#doc_pdm)
- `set_angle(angle: int)` - Устанавливает угол сервопривода, в диапазоне `min_angle < angle < max_angle` (или `max_angle < angle < min_angle` если `min_angle > max_angle`).
- `release()` - Устанавливает длительность импульса в 0, тем самым отключая удержание позиции сервоприводом.
- `deinit()` - Отключает PWM генерацию.

### Методы класса ServoPDMRP2Async и ServoPDMRP2Irq
Ну один метод, если быть точным :).
- `move_to_angle(...)` - Плавно перемещает сервопривод до указанного угла.

| Параметр        | Тип                   | По умолчанию | Описание                                                      |
|-----------------|-----------------------|--------------|---------------------------------------------------------------|
| angle           | Int                   | None         | Конечный угол поворота                                        |
| time_ms         | Int                   | None         | Время движения                                                |
| start_smoothing | type(ServoSmoothBase) | SmoothLinear | Класс замедления который будет использован для движения       |
| callback        | callable              | None         | Функция которая будет вызвана после окончания работы команды. |


### Замедления
Для управления замедлениями можно использовать классы `ServoSmoothBase` и его наследников.
В данной библиотеке есть только линейное замедление `SmoothLinear`, если вам требуется больше, установите библиотеку [smooth-servo](https://pypi.org/project/smooth-servo/).
Пример использования встроенного замедления:
```python
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Async, SmoothLinear

# создаем PWM контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# создаем объект сервопривода
servo = ServoPDMRP2Async(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)

# Повернуть сервопривод до отметки в 50 градусов за 2 секунды используя линейное замедление. После вывести в консоль "callback cv"
servo.move_to_angle(50, 2000, SmoothLinear, callback=lambda: print("callback move_to_angle"))
```
Подробно про параметры и типы замедлений можно прочитать в [документации к smooth_servo](https://github.com/TTitanUA/smooth_servo#doc).


## Примеры
Примеры использования можно найти в папке [examples](https://github.com/TTitanUA/micropython_servo_pdm/tree/main/examples).

<a id="feedback"></a>
## Баги и обратная связь
При нахождении багов создавайте [issue](https://github.com/TTitanUA/micropython_servo_pdm/issues)
Библиотека открыта для доработки и ваших [pull запросов](https://github.com/TTitanUA/micropython_servo_pdm/pulls)!
