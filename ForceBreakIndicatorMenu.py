import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from typing import *
from datetime import datetime

from AppState import AppState
from Clock import Clock, AlarmClock, TimerClock

class ForceBreakIndicatorMenu(Gtk.Menu):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "quit-activated": (GObject.SignalFlags.RUN_FIRST, None, tuple())
    }
    def __init__(self, app_state = AppState()):
        super().__init__()
        self._app_state = app_state

        self._time_left_item = Gtk.MenuItem(sensitive=False)
        self._quit_item = Gtk.MenuItem(label="Quit")

        self.add(self._time_left_item)
        self.add(self._quit_item)
        self.update_ui()
        self._connect_signals()
        self.show_all()

    def _connect_signals(self):
        self._quit_item.connect("activate", self._on_quit)
        self.connect('focus', self._on_focus)

    def _on_quit(self, widget):
        self.emit("quit-activated")

    def _on_focus(self, *args):
        self.update_ui()

    def update_ui(self):
        if self._app_state.clock is None:
            self._time_left_item.set_label("Clock is not picked")
        else:
            self._time_left_item.set_label("Time left: %s" % self._app_state.timer_clock)

