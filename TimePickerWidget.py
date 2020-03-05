import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from typing import Tuple, Union, Any, Dict
from datetime import datetime, timedelta

from Clock import TimerClock, AlarmClock

class TimePickerWidget(Gtk.HBox):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "changed": (GObject.SignalFlags.RUN_LAST, None, tuple()),
    }

    def __init__(self, hours=0, minutes=0, **kwargs):
        super().__init__(**kwargs)

        self._hours_input = Gtk.SpinButton.new_with_range(0, 23, 1)
        self._hours_input.set_value(hours)
        self._hours_input.set_wrap(True)

        self._minutes_input = Gtk.SpinButton.new_with_range(0, 59, 5)
        self._minutes_input.set_value(minutes)
        self._minutes_input.set_wrap(True)

        self._init_layout()
        self._connect_signals()

    def _init_layout(self):
        self.pack_start(self._hours_input, False, False, 0)
        self.pack_start(Gtk.Label(label=" h  "), False, True, 0)
        self.pack_start(self._minutes_input, False, False, 0)
        self.pack_start(Gtk.Label(label=" m  "), False, True, 0)

    def _connect_signals(self):
        try:
            if self._connected_signals:
                return
        except AttributeError:
            self._hours_input.connect('value-changed', self._value_changed_callback)
            self._minutes_input.connect('value-changed', self._value_changed_callback)
            self._connected_signals = True

    def _value_changed_callback(self, sender):
        self.emit('changed')
        
    def get_hours(self) -> int:
        return int(self._hours_input.get_value())

    def get_minutes(self) -> int:
        return int(self._minutes_input.get_value())
    
    def set_hours(self, value):
        self._hours_input.set_value(value)

    def set_minutes(self, value):
        self._minutes_input.set_value(value)

    def set_hours_and_minutes(self, hours: int, minutes: int):
        self._hours_input.set_value(hours)
        self._minutes_input.set_value(minutes)

    def get_as_datetime(self, now = datetime.now()) -> datetime:
        return now.replace(hour = self.get_hours(), minutes = self.get_minutes())

    def get_as_timedelta(self) -> timedelta:
        return timedelta(hours = self.get_hours(), minutes = self.get_minutes()) 

    def get_as_timer_clock(self) -> TimerClock:
        return TimerClock(self.get_as_timedelta())

    def get_as_alarm_clock(self) -> AlarmClock:
        return AlarmClock(self.get_as_datetim())

    def get_hours_and_minutes(self) -> Tuple[int, int]:
        return self.get_hours(), self.get_minutes()
