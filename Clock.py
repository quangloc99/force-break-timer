import gi
from gi.repository import GObject

from typing import Tuple, Union
from datetime import datetime, timedelta

class Clock(GObject.Object):
    hours = GObject.Property(type=int)
    minutes = GObject.Property(type=int)
    seconds = GObject.Property(type=int)
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        super().__init__()
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def get_hours_and_minutes(self) -> Tuple[int, int]:
        return self.hours, self.minutes

    def set_hours_and_minutes(self, hours: int, minutes: int):
        self.hours, self.minutes = hours, minutes

    def get_hours_minutes_and_seconds(self) -> Tuple[int, int, int]:
        return self.hours, self.minutes, self.seconds

    def set_hours_minutes_and_seconds(self, hours: int, minutes: int, seconds: int):
        self.hours, self.minutes, self.seconds = hours, minutes, seconds

    def __eq__(self, other):
        return self.hours == other.hours and self.minutes == other.minutes and self.seconds == other.seconds
    
    # this is python3 but somehow this does not called.
    # I guess that one of the reasons is GObject
    def __ne__(self, other): 
        return not (self == other) 

    def __str__(self):
        return "{:0>2}:{:0>2}:{:0>2}".format(*self.get_hours_minutes_and_seconds())

    def make_same_as(self, other):
        return self.as_alarm_clock() if isinstance(other, AlarmClock) else self.as_timer_clock()

    def to_same_as(self, other, now):
        return self.to_alarm_clock(now) if isinstance(other, AlarmClock) else self.to_timer_clock(now)


class TimerClock(Clock):
    clock_type = GObject.Property(type=str, default="Timer")

    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        super().__init__(hours, minutes, seconds)

    @classmethod
    def new(cls, duration: timedelta):
        res = TimerClock()
        res.duration = duration
        return res

    @GObject.Property(type=object)
    def duration(self) -> timedelta:
        return timedelta(hours = self.hours, minutes = self.minutes, seconds = self.seconds)

    @duration.setter
    def set_duration(self, value: timedelta):
        self.minutes, self.seconds = divmod(value.seconds, 60)
        self.hours, self.minutes = divmod(self.minutes, 60)

    def get_time_left(self, now: datetime = datetime.now()) -> timedelta:
        return self.duration

    def to_timer_clock(self, now: datetime = datetime.now()) -> 'TimerClock':
        return self

    def to_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return AlarmClock.new(now + self.duration)

    def as_timer_clock(self):
        return self

    def as_alarm_clock(self):
        return AlarmClock(self.hours, self.minutes, self.seconds)

    def to_compliment(self, now: datetime = datetime.now()):
        return self.to_alarm_clock(now)

class AlarmClock(Clock):
    clock_type = GObject.Property(type=str, default='Alarm')

    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        super().__init__(hours, minutes)

    @classmethod
    def new(cls, alarm_time: datetime):
        res = AlarmClock()
        res.alarm_time = alarm_time
        return res

    @GObject.Property(type=object)
    def alarm_time(self):
        return datetime.now().replace(hour = self.hours, minute = self.minutes, second = self.seconds)

    @alarm_time.setter
    def set_alarm_time(self, value: datetime):
        self.hours, self.minutes, self.seconds = value.hour, value.minute, value.second

    def get_time_left(self, now: datetime = datetime.now()) -> timedelta:
        return self.alarm_time - now

    def to_timer_clock(self, now: datetime = datetime.now()) -> 'TimerClock':
        return TimerClock.new(self.alarm_time - now);

    def to_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return self

    def as_timer_clock(self):
        return TimerClock(self.hours, self.minutes, self.seconds)

    def as_alarm_clock(self):
        return self

    def to_compliment(self, now: datetime = datetime.now()):
        return self.to_timer_clock(now)

