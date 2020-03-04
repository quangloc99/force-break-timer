import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from typing import *
from datetime import datetime

from Clock import TimerClock, AlarmClock, ClockType
from TimePickerWidget import TimePickerWidget

class NotifyClockPickerWidget(Gtk.Grid):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "picked": (GObject.SignalFlags.RUN_FIRST, None, (object, ))
    }

    def __init__(self, clock: ClockType = TimerClock(), now: datetime = datetime.now(), **kwargs):
        super().__init__(row_spacing=10, column_spacing=5, **kwargs)
        self.clock = clock
        self._now = now

        self._mode_switch_button = Gtk.Button(label="Switch", hexpand=False, halign=Gtk.Align.END)
        self._mode_label = Gtk.Label(hexpand=False, halign=Gtk.Align.START)

        self._timer_picker = TimePickerWidget()
        self._alarm_picker = TimePickerWidget()
        self._set_clock_button= Gtk.Button(label="Set", margin_top=10)

        self._init_layout()
        self._update_ui()
        self._connect_signals()

    def _init_layout(self):
        # for easily adding elements
        self._current_row = 0  
        self._current_column = 0

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

    def _add_elm(self, widget: Optional[Gtk.Widget], width: int):
        if widget is not None:
            self.attach(widget, self._current_column, self._current_row, width, 1)
        self._current_column += width

    def _connect_signals(self):
        self._mode_switch_button.connect('clicked', self._switch_mode)
        self._timer_picker.connect('changed', self._timer_picker_callback)
        self._alarm_picker.connect('changed', self._alarm_picker_callback)
        self._set_clock_button.connect('clicked', self._set_clock_button_callback)

    def _timer_picker_callback(self, time_picker: TimePickerWidget):
        if not isinstance(self.clock, TimerClock):
            return 
        self.clock.set_hours_and_minutes(*time_picker.get_hours_and_minutes())
        self._update_ui_for_alarm()

    def _alarm_picker_callback(self, time_picker: TimePickerWidget):
        if not isinstance(self.clock, AlarmClock):
            return
        self.clock.set_hours_and_minutes(*time_picker.get_hours_and_minutes())
        self._update_ui_for_timer()

    def _set_clock_button_callback(self, button: Gtk.Button):
        self.emit('picked', self.clock)

    def _switch_mode(self, x):
        if isinstance(self.clock, TimerClock):
            self.clock = self.clock.to_alarm_clock(self._now)
        else:
            self.clock = self.clock.to_timer_clock(self._now)
        self._update_ui_mode()

    def _update_ui(self):
        self._update_ui_for_alarm()
        self._update_ui_for_timer()
        self._update_ui_mode()

    def _update_ui_for_alarm(self):
        self._alarm_picker.set_hours_and_minutes(*self.get_alarm_clock().get_hours_and_minutes())

    def _update_ui_for_timer(self):
        self._timer_picker.set_hours_and_minutes(*self.get_timer_clock().get_hours_and_minutes())

    def _update_ui_mode(self):
        self._alarm_picker.set_sensitive(isinstance(self.clock, AlarmClock))
        self._timer_picker.set_sensitive(isinstance(self.clock, TimerClock))
        self._mode_label.set_label(self.clock.get_clock_type())

    def _new_row(self):
        self._current_row += 1
        self._current_column = 0

    def update_time(self):
        now = datetime.now()
        self.current_time = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)

    def set_now(self, now: datetime = datetime.now()):
        self._now = now
        self.update_ui()

    def get_timer_clock(self) -> TimerClock:
        return self.clock if isinstance(self.clock, TimerClock) else self.clock.to_timer_clock(self._now)

    def get_alarm_clock(self) -> AlarmClock:
        return self.clock if isinstance(self.clock, AlarmClock) else self.clock.to_alarm_clock(self._now)

