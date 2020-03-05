import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from typing import *
from datetime import datetime

from AppState import AppState
from Clock import TimerClock, AlarmClock
from TimePickerWidget import TimePickerWidget

class NotifyClockPickerWidget(Gtk.Grid):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "picked": (GObject.SignalFlags.RUN_FIRST, None, (object, ))
    }

    def __init__(self, app_state: AppState = AppState(), **kwargs):
        super().__init__(row_spacing=10, column_spacing=5, **kwargs)

        self._app_state = app_state

        self._editing_clock = app_state.clock
        self._now_label = Gtk.Label(hexpand=False, halign=Gtk.Align.START)

        self._mode_switch_button = Gtk.Button(label="Switch", hexpand=False, halign=Gtk.Align.END)
        self._mode_label = Gtk.Label(hexpand=False, halign=Gtk.Align.START)

        self._timer_picker = TimePickerWidget()
        self._alarm_picker = TimePickerWidget()
        self._set_clock_button= Gtk.Button(label="Set", margin_top=10)

        self._init_layout()
        self.update_ui()
        self._connect_signals()

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

        self._add_elm(None, 2)
        self._add_elm(self._set_clock_button, 1)
        self._new_row()

    def _add_elm(self, widget: Optional[Gtk.Widget], width: int):
        if widget is not None:
            self.attach(widget, self._current_column, self._current_row, width, 1)
        self._current_column += width

    def _new_row(self):
        self._current_row += 1
        self._current_column = 0

    def _connect_signals(self):
        self._app_state.bind_property('now_str', self._now_label, 'label', GObject.BindingFlags.SYNC_CREATE)
        self._mode_switch_button.connect('clicked', self._switch_mode)
        self._timer_picker.connect('changed', self._timer_picker_callback)
        self._alarm_picker.connect('changed', self._alarm_picker_callback)
        self._set_clock_button.connect('clicked', self._set_clock_button_callback)

    def _timer_picker_callback(self, time_picker: TimePickerWidget):
        if not isinstance(self._editing_clock, TimerClock):
            return 
        self._editing_clock = time_picker.timer_clock
        self._update_ui_for_alarm()

    def _alarm_picker_callback(self, time_picker: TimePickerWidget):
        if not isinstance(self._editing_clock, AlarmClock):
            return
        self._editing_clock = time_picker.alarm_clock
        self._update_ui_for_timer()

    def _set_clock_button_callback(self, button: Gtk.Button):
        self.emit('picked', self._editing_clock)

    def _switch_mode(self, x):
        if isinstance(self._editing_clock, TimerClock):
            self._editing_clock = self._editing_clock.as_alarm_clock(self._app_state.now)
        else:
            self._editing_clock = self._editing_clock.as_timer_clock(self._app_state.now)
        self._update_ui_mode()

    def update_ui(self):
        # self._now_label.set_label(self._app_state.get_now_str()) 
        self._update_ui_for_alarm()
        self._update_ui_for_timer()
        self._update_ui_mode()

    def _update_ui_for_alarm(self):
        self._alarm_picker.alarm_clock = self._editing_clock.as_alarm_clock(self._app_state.now)

    def _update_ui_for_timer(self):
        self._timer_picker.timer_clock = self._editing_clock.as_timer_clock(self._app_state.now)

    def _update_ui_mode(self):
        self._alarm_picker.set_sensitive(isinstance(self._editing_clock, AlarmClock))
        self._timer_picker.set_sensitive(isinstance(self._editing_clock, TimerClock))
        self._mode_label.set_label(self._editing_clock.clock_type)

