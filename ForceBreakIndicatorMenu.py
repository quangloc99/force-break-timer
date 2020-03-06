import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from typing import *
from datetime import datetime

from AppState import AppState
from Clock import Clock, AlarmClock, TimerClock

class ForceBreakIndicatorMenu(Gtk.Menu):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "quit-activated": (GObject.SignalFlags.RUN_FIRST, None, tuple()),
    }

    now = GObject.Property()
    running_clock = GObject.Property()

    def __init__(self, now = datetime.now(), running_clock = AlarmClock()):
        super().__init__()

        self.now = now
        self.running_clock = running_clock

        self._time_left_item = Gtk.MenuItem(sensitive=False)
        self._quit_item = Gtk.MenuItem(label="Quit")

        self.add(self._time_left_item)
        self.add(self._quit_item)
        self._connect_signals()
        self.show_all()

    def _connect_signals(self):
        self._quit_item.connect("activate", self._on_quit)

        self.connect("notify::now", self._update_clock_labels)
        self.connect("notify::running-clock", self._update_clock_labels)

    def _on_quit(self, widget):
        self.emit("quit-activated")

    def _update_clock_labels(self, *args):
        if self.running_clock is None:
            self._time_left_item.set_label("Clock is not picked")
        else:
            self._time_left_item.set_label("Time left: %s" % 
                    self.running_clock.to_timer_clock(self.now))

