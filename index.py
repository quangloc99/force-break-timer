import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from typing import *

from Clock import ClockType
from NotifyClockPickerWidget import NotifyClockPickerWidget

css = b"""
    .header {
        font-size: 30px;
    }
"""

css_provider= Gtk.CssProvider()
css_provider.load_from_data(css)
Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class AppWindow(Gtk.Window):
    def __init__(self, **kwargs):
        super().__init__(title="Force break", **kwargs)

        header = Gtk.Label(label="Time to set a new timer", hexpand=False, halign=Gtk.Align.CENTER, valign = Gtk.Align.CENTER) 
        header.get_style_context().add_class('header') 

        # If someone reading this code and know how to do this, tell me the other way to center this element.
        # I am using Ubuntu with i3, and I could not found the other way.
        self._clock_picker = NotifyClockPickerWidget()
        box1, box2 = Gtk.HBox(), Gtk.VBox()
        box1.set_center_widget(self._clock_picker)
        box2.set_center_widget(box1)
        self.add(box2)

        box2.pack_start(header, True, True, 0)
        box2.pack_end(Gtk.Button(label="Quit", halign=Gtk.Align.START), False, False, 0)

        self._connect_signals()

    def _connect_signals(self):
        self._clock_picker.connect('picked', self._accept_new_clock)

    def _accept_new_clock(self, widget: NotifyClockPickerWidget, clock: ClockType):
        print(*clock.get_hours_and_minutes())

win = AppWindow()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()

