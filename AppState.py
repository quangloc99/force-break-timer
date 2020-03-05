import gi
from gi.repository import GObject

from typing import *
from datetime import datetime

from Clock import Clock, TimerClock, AlarmClock

class AppState(GObject.Object):
    def __init__(self, clock: Clock = TimerClock()):
        super().__init__()
        self._picked_clock = clock.as_alarm_clock(self.now)
        self._running_clock = None

    @GObject.Property(type=object)
    def picked_clock(self):
        return self._picked_clock

    @picked_clock.setter
    def set_picked_clock(self, value):
        self._picked_clock = value

    def switch_picked_clock_mode(self):
        if isinstance(self._picked_clock, TimerClock):
            self.picked_clock = self._picked_clock.as_alarm_clock(self.now)
        else:
            self.picked_clock = self._picked_clock.as_timer_clock(self.now)

    @GObject.Property(type=object)
    def running_clock(self) -> datetime:
        return self._running_clock

    @GObject.Property(type=object)
    def now(self) -> datetime:
        return datetime.now()

    @GObject.Property(type=str)
    def now_str(self) -> str:
        return "{:0>2}:{:0>2}".format(self.now.hour, self.now.minute)

    @GObject.Property(type=object)
    def timer_clock(self) -> TimerClock:
        return self._clock.as_timer_clock(self.now)

    @GObject.Property(type=object)
    def alarm_clock(self) -> AlarmClock:
        return self._clock.as_alarm_clock(self.now)


