import gi
from gi.repository import GObject

from typing import *
from datetime import datetime

from Clock import Clock, TimerClock, AlarmClock

class AppState(GObject.Object):
    def __init__(self, clock: Clock = TimerClock()):
        super().__init__()
        self._clock = clock.as_alarm_clock(self.now)

    @GObject.Property(type=object)
    def clock(self):
        return self._clock

    @clock.setter
    def set_clock(self, value):
        self._clock = value

    @GObject.Property(type=object)
    def now(self) -> datetime:
        return datetime.now()

    def get_now_str(self) -> str:
        return "{:0>2}:{:0>2}".format(self.now.hour, self.now.minute)

    @GObject.Property(type=object)
    def timer_clock(self) -> TimerClock:
        return self._clock.as_timer_clock(self.now)

    @GObject.Property(type=object)
    def alarm_clock(self) -> AlarmClock:
        return self._clock.as_alarm_clock(self.now)


