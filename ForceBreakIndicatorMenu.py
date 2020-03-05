import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from typing import *
from datetime import datetime

from Clock import ClockType, AlarmClock, TimerClock

class ForceBreakIndicatorMenu(Gtk.Menu):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "quit-activated": (GObject.SignalFlags.RUN_FIRST, None, tuple())
    }
    def __init__(self, clock: Optional[ClockType] = None, now: datetime = datetime.now()):
        super().__init__()
        self._now = now
        self._clock = clock

        self._time_left_item = Gtk.MenuItem(sensitive=False)
        self._quit_item = Gtk.MenuItem(label="Quit")

        self.add(self._time_left_item)
        self.add(self._quit_item)
        self._update_ui()
        self._connect_signals()
        self.show_all()

    def _connect_signals(self):
        self._quit_item.connect("activate", self._on_quit)

    def _on_quit(self, widget):
        self.emit("quit-activated")

    def _update_ui(self):
        if self._clock is None:
            self._time_left_item.set_label("Clock is not picked")
        else:
            self._time_left_item.set_label("Time left: %s" % self._clock.as_timer_clock(self._now))

    def set_clock(self, clock: Optional[ClockType]):
        self._clock = clock.as_alarm_clock() if clock is not None else None
        self._update_ui()

    def set_now(self, now: datetime = datetime.now()):
        self._now = now
        self._update_ui()
