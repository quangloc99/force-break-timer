import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from typing import *
from datetime import datetime

from AppState import AppState
from Clock import Clock
from NotifyClockPickerWidget import NotifyClockPickerWidget

class AppWindow(Gtk.Window):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "quit": (GObject.SignalFlags.RUN_FIRST, None, tuple()),
            "clock-picked": (GObject.SignalFlags.RUN_FIRST, None, (Clock, )),
    }

    def __init__(self,  **kwargs):
        super().__init__(title="Force break", **kwargs)

        self._clock_picker = NotifyClockPickerWidget()
        self._set_button = Gtk.Button(label="Set", valign=Gtk.Align.START)
        self._quit_button = Gtk.Button(label="Quit", halign=Gtk.Align.START, valign=Gtk.Align.END)

        self._init_layout()
        self._connect_signals()

    @GObject.Property
    def now(self):
        return self._clock_picker.now

    @GObject.Property
    def picking_clock(self):
        return self._clock_picker.picking_clock

    @now.setter
    def set_now(self, value):
        self._clock_picker.now = value

    @picking_clock.setter
    def set_picking_clock(self, value):
        self._clock_picker.picking_clock = value

    def _init_layout(self):
        header = Gtk.Label(label="Time to set a new timer", hexpand=False, halign=Gtk.Align.CENTER, valign = Gtk.Align.CENTER) 
        header.get_style_context().add_class('header') 

        # If someone reading this code and know how to do this, tell me the other way to center this element.
        # I am using Ubuntu with i3, and I could not found the other way.
        box1, box2 = Gtk.VBox(), Gtk.HBox()
        box1.set_center_widget(self._clock_picker)
        box2.set_center_widget(box1)
        self.add(box2)

        box1.pack_start(header, True, True, 0)
        box1.pack_end(self._set_button, True, True, 20)
        box2.pack_start(self._quit_button, False, False, 0)

    def _connect_signals(self):
        self._set_button.connect('clicked', self._accept_new_clock)
        self._quit_button.connect('clicked', self._on_quit)

    def _accept_new_clock(self, widget):
        self.emit('clock-picked', self.picking_clock)

    def _on_quit(self, *args):
        self.emit("quit")

