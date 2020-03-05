from typing import Tuple, Union
from datetime import datetime, timedelta

class TimerClock:
    def __init__(self, duration: timedelta = timedelta(minutes=25)) -> None:
        self.duration = duration

    def get_clock_type(self):
        return 'Timer'

    def to_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return AlarmClock(now + self.duration)

    def set_hours_and_minutes(self, hours: int, minutes: int):
        self.duration = timedelta(hours = hours, minutes = minutes)

    def get_hours_and_minutes(self) -> Tuple[int, int]:
        return divmod(self.duration.seconds // 60, 60)

    def get_time_left(self, now: datetime = datetime.now()) -> timedelta:
        return self.duration

    def as_timer_clock(self, now: datetime = datetime.now()) -> 'TimerClock':
        return self

    def as_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return self.to_alarm_clock(now)

    def __str__(self):
        return "{:0>2}:{:0>2}".format(*self.get_hours_and_minutes())

class AlarmClock:
    def __init__(self, alarm_time: datetime = datetime.now()) -> None:
        self.alarm_time = alarm_time

    def get_clock_type(self):
        return 'Alarm'

    def to_timer_clock(self, now: datetime = datetime.now()) -> 'TimerClock':
        return TimerClock(self.alarm_time - now);

    def set_hours_and_minutes(self, hours: int, minutes: int):
        self.alarm_time = self.alarm_time.replace(hour = hours, minute = minutes)

    def get_hours_and_minutes(self) -> Tuple[int, int]:
        return self.alarm_time.hour, self.alarm_time.minute
    
    def get_time_elft(self, now: datetime = datetime.now()) -> timedelta:
        return self.alarm_time - now

    def as_timer_clock(self, now: datetime = datetime.now()) -> 'TimerClock':
        return self.to_timer_clock(now)

    def as_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return self

    def __str__(self):
        return "{:0>2}:{:0>2}".format(*self.get_hours_and_minutes())

ClockType = Union[TimerClock, AlarmClock]
