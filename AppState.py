from typing import *
from datetime import datetime

from Clock import ClockType, TimerClock, AlarmClock

class AppState:
    def __init__(self, clock: ClockType = TimerClock()):
        self._clock: AlarmClock = clock.as_alarm_clock(self.get_now())

    def get_now(self) -> datetime:
        return datetime.now()

    def get_now_str(self) -> str:
        now = self.get_now()
        return "{:0>2}:{:0>2}".format(now.hour, now.minute)

    def get_clock(self) -> ClockType:
        return self._clock

    def set_clock(self, clock: ClockType) -> None:
        self._clock = clock.as_alarm_clock(self.get_now())

    def get_timer_clock(self) -> TimerClock:
        return self._clock.as_timer_clock(self.get_now())

    def get_alarm_clock(self) -> AlarmClock:
        return self._clock.as_alarm_clock(self.get_now())


