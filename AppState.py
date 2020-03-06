import gi
from gi.repository import GObject

from typing import *
from datetime import datetime

from Clock import Clock, TimerClock, AlarmClock

class AppState(GObject.Object):
    def __init__(self, clock: Clock = TimerClock(), now = datetime.now()):
        super().__init__()
        self._now = now
        self._picked_clock = clock.to_alarm_clock(self.now)
        self._running_clock = None

    @GObject.Property(type=object)
    def picked_clock(self):
        return self._picked_clock

    @picked_clock.setter
    def set_picked_clock(self, value):
        self._picked_clock = value

    @GObject.Property(type=object)
    def running_clock(self) -> datetime:
        return self._running_clock

    @GObject.Property(type=object)
    def now(self) -> datetime:
        return self._now

    def reset_running_clock(self):
        self._running_clock = self._picked_clock.to_alarm_clock(self._now)
        print(self._running_clock)
        print(self._running_clock.to_timer_clock(self._now))
        self.notify('running-clock')

    def remove_running_clock(self):
        self._running_clock = None
        self.notify('running-clock')

    def reset_now(self):
        self._now = datetime.now()
        self.notify('now')
