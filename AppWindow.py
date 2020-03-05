import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from typing import *
from datetime import datetime

from AppState import AppState
from Clock import ClockType
from NotifyClockPickerWidget import NotifyClockPickerWidget

class AppWindow(Gtk.Window):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "quit": (GObject.SignalFlags.RUN_FIRST, None, tuple())
    }

    def __init__(self, app_state: AppState = AppState(), **kwargs):
        super().__init__(title="Force break", **kwargs)

        self._app_state = app_state

        self._clock_picker = NotifyClockPickerWidget(app_state = app_state)
        self._quit_button = Gtk.Button(label="Quit", halign=Gtk.Align.START)

        self._init_layout()
        self._connect_signals()

    def _init_layout(self):
        header = Gtk.Label(label="Time to set a new timer", hexpand=False, halign=Gtk.Align.CENTER, valign = Gtk.Align.CENTER) 
        header.get_style_context().add_class('header') 

        # If someone reading this code and know how to do this, tell me the other way to center this element.
        # I am using Ubuntu with i3, and I could not found the other way.
        box1, box2 = Gtk.HBox(), Gtk.VBox()
        box1.set_center_widget(self._clock_picker)
        box2.set_center_widget(box1)
        self.add(box2)

        box2.pack_start(header, True, True, 0)
        box2.pack_end(self._quit_button, False, False, 0)

    def _connect_signals(self):
        self._clock_picker.connect('picked', self._accept_new_clock)
        self._quit_button.connect('clicked', self._on_quit)

    def _accept_new_clock(self, widget: NotifyClockPickerWidget, clock: ClockType):
        print(*clock.get_hours_and_minutes())

    def _on_quit(self, *args):
        self.emit("quit")
