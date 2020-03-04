from typing import Tuple, Union
from datetime import datetime, timedelta

class TimerClock:
    def __init__(self, duration: timedelta = timedelta(minutes=25)) -> None:
        self.duration = max(duration, timedelta())

    def get_clock_type(self):
        return 'Timer'

    def to_alarm_clock(self, now: datetime = datetime.now()) -> 'AlarmClock':
        return AlarmClock(now + self.duration)

    def set_hours_and_minutes(self, hours: int, minutes: int):
        self.duration = timedelta(hours = hours, minutes = minutes)

    def get_hours_and_minutes(self) -> Tuple[int, int]:
        return divmod(self.duration.seconds // 60, 60)

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

ClockType = Union[TimerClock, AlarmClock]
