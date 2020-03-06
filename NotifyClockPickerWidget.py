import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from typing import *
from datetime import datetime

from AppState import AppState
from Clock import TimerClock, AlarmClock
from TimePickerWidget import TimePickerWidget
from helper import bind_property_full

class NotifyClockPickerWidget(Gtk.Grid):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "switched": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, now = datetime.now(), picking_clock = TimerClock(), **kwargs):
        super().__init__(row_spacing=10, column_spacing=5, **kwargs)

        self._now = now
        self._picking_clock = picking_clock

        self._now_label = Gtk.Label(hexpand=False, halign=Gtk.Align.START)

        self._mode_switch_button = Gtk.Button(label="Switch", hexpand=False, halign=Gtk.Align.END)
        self._mode_label = Gtk.Label(hexpand=False, halign=Gtk.Align.START)

        self._timer_picker = TimePickerWidget()
        self._alarm_picker = TimePickerWidget()

        self._init_layout()
        self._connect_signals()

    @GObject.Property
    def picking_clock(self):
        return self._picking_clock

    @GObject.Property
    def now(self):
        return self._now

    @picking_clock.setter
    def set_picking_clock(self, value):
        self._picking_clock = value

    @now.setter
    def set_now(self, value):
        self._now = value

    def _init_layout(self):
        # for easily adding elements
        self._current_row = 0  
        self._current_column = 0

        self._add_elm(Gtk.Label(label = "Now is: ", halign=Gtk.Align.END), 1)
        self._add_elm(self._now_label, 2)
        self._new_row()

        self._add_elm(Gtk.Label(label = "Mode: ", halign=Gtk.Align.END), 1)
        self._add_elm(self._mode_label, 1)
        self._add_elm(self._mode_switch_button, 1)
        self._new_row()

        self._add_elm(Gtk.Label(label = "Time left: ", halign=Gtk.Align.END), 1)
        self._add_elm(self._timer_picker, 2)
        self._new_row()

        self._add_elm(Gtk.Label(label = "Notify at: ", halign=Gtk.Align.END), 1)
        self._add_elm(self._alarm_picker, 2)
        self._new_row()

    def _add_elm(self, widget: Optional[Gtk.Widget], width: int):
        if widget is not None:
            self.attach(widget, self._current_column, self._current_row, width, 1)
        self._current_column += width

    def _new_row(self):
        self._current_row += 1
        self._current_column = 0

    def _connect_signals(self):
        bind_property_full(self, 'now', self._now_label, 'label', GObject.BindingFlags.SYNC_CREATE,
                lambda now: "{:0>2}:{:0>2}".format(now.hour, now.minute))
        bind_property_full(self, 'picking-clock', self._mode_label, 'label', GObject.BindingFlags.SYNC_CREATE,
                lambda clock: clock.clock_type)
        bind_property_full(self, 'picking-clock', self._alarm_picker, 'sensitive', GObject.BindingFlags.SYNC_CREATE, 
                lambda clock: isinstance(clock, AlarmClock)) 
        bind_property_full(self, 'picking-clock', self._timer_picker, 'sensitive', GObject.BindingFlags.SYNC_CREATE, 
                lambda clock: isinstance(clock, TimerClock)) 

        bind_property_full(self, 'picking-clock', self._alarm_picker, 'alarm-clock', GObject.BindingFlags.BIDIRECTIONAL,   
                lambda clock: clock.to_alarm_clock(self._now),   
                lambda alarm_clock: alarm_clock.to_same_as(self.picking_clock, self._now))   
        bind_property_full(self, 'picking-clock', self._timer_picker, 'timer-clock', GObject.BindingFlags.BIDIRECTIONAL, 
                lambda clock: clock.to_timer_clock(self._now), 
                lambda timer_clock: timer_clock.to_same_as(self._picking_clock, self._now))

        self._mode_switch_button.connect('clicked', self._switch_mode)

    def _switch_mode(self, x):
        self.picking_clock = self._picking_clock.to_compliment(self._now)
        self.emit('switched')

