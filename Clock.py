import gi
from gi.repository import GObject

from typing import Tuple, Union
from datetime import datetime, timedelta

class Clock(GObject.Object):
    hours = GObject.Property(type=int)
    minutes = GObject.Property(type=int)
    def __init__(self, hours: int = 0, minutes: int = 0):
        super().__init__()
        self.hours = hours
        self.minutes = minutes

    def __str__(self):
        return "{:0>2}:{:0>2}".format(*self.get_hours_and_minutes())

    def get_hours_and_minutes(self) -> Tuple[int, int]:
        return self.hours, self.minutes

    def set_hours_and_minutes(self, hours: int, minutes: int):
        self.hours, self.minutes = hours, minutes


class TimerClock(Clock):
    clock_type = GObject.Property(type=str, default="Timer")

    def __init__(self, hours: int = 0, minutes: int = 0):
        super().__init__(hours, minutes)

    @classmethod
    def new(cls, duration: timedelta):
        res = TimerClock()
        res.duration = duration
        return res

    @GObject.Property(type=object)
    def duration(self) -> timedelta:
        return timedelta(hours = self.hours, minutes = self.minutes)

    @duration.setter
    def set_duration(self, value: timedelta):
        self.hours, self.minutes = divmod(value.seconds // 60, 60)

    def get_time_left(self, now: datetime = datetime.now()) -> timedelta:
        return self.duration

    def as_timer_clock(self, now: datetime = datetime.now()) -> 'TimerClock':
        return self

    def as_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return AlarmClock.new(now + self.duration)

class AlarmClock(Clock):
    clock_type = GObject.Property(type=str, default='Alarm')

    def __init__(self, hours: int = 0, minutes: int = 0):
        super().__init__(hours, minutes)

    @classmethod
    def new(cls, alarm_time: datetime):
        res = AlarmClock()
        res.alarm_time = alarm_time
        return res

    @GObject.Property(type=object)
    def alarm_time(self):
        return datetime.now().replace(hour = self.hours, minute = self.minutes)

    @alarm_time.setter
    def set_alarm_time(self, value: datetime):
        self.hours, self.minutes = value.hour, value.minute

    def get_time_left(self, now: datetime = datetime.now()) -> timedelta:
        return self.alarm_time - now

    def as_timer_clock(self, now: datetime = datetime.now()) -> 'TimerClock':
        return TimerClock.new(self.alarm_time - now);

    def as_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return self

