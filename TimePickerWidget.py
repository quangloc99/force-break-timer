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

    def __init__(self, hours=0, minutes=0, seconds=0, **kwargs):
        super().__init__(**kwargs)

        self._hours_input = Gtk.SpinButton.new_with_range(0, 23, 1)
        self._hours_input.set_value(hours)
        self._hours_input.set_wrap(True)

        self._minutes_input = Gtk.SpinButton.new_with_range(0, 59, 5)
        self._minutes_input.set_value(minutes)
        self._minutes_input.set_wrap(True)

        self._seconds_input = Gtk.SpinButton.new_with_range(0, 59, 5)
        self._seconds_input.set_value(seconds)
        self._seconds_input.set_wrap(True)

        self._init_layout()
        self._connect_signals()

    def _init_layout(self):
        self.pack_start(self._hours_input, False, False, 0)
        self.pack_start(Gtk.Label(label=" h  "), False, True, 0)
        self.pack_start(self._minutes_input, False, False, 0)
        self.pack_start(Gtk.Label(label=" m  "), False, True, 0)
        self.pack_start(self._seconds_input, False, False, 0)
        self.pack_start(Gtk.Label(label=" s  "), False, True, 0)

    def _connect_signals(self):
        self._hours_input.connect('value-changed', self._hours_changed_callback)
        self._minutes_input.connect('value-changed', self._minutes_changed_callback)
        self._seconds_input.connect('value-changed', self._seconds_changed_callback)

    def _hours_changed_callback(self, sender):
        self.notify('hours')
        self.notify('timer_clock')
        self.notify('alarm_clock')
        self.emit('changed')

    def _minutes_changed_callback(self, sender):
        self.notify('minutes')
        self.notify('timer_clock')
        self.notify('alarm_clock')
        self.emit('changed')

    def _seconds_changed_callback(self, sender):
        self.notify('seconds')
        self.notify('timer_clock')
        self.notify('alarm_clock')
        self.emit('changed')
        
    @GObject.Property(type=int)
    def hours(self) -> int:
        return int(self._hours_input.get_value())

    @GObject.Property(type=int)
    def minutes(self) -> int:
        return int(self._minutes_input.get_value())

    @GObject.Property(type=int)
    def seconds(self) -> int:
        return int(self._seconds_input.get_value())
    
    @hours.setter
    def set_hours(self, value):
        self._hours_input.set_value(value)

    @minutes.setter
    def set_minutes(self, value):
        self._minutes_input.set_value(value)

    @seconds.setter
    def set_seconds(self, value):
        self._seconds_input.set_value(value)

    def get_hours_minutes_and_seconds(self) -> Tuple[int, int]:
        return self.hours, self.minutes, self.seconds

    def set_hours_minutes_and_seconds(self, hours: int, minutes: int, seconds: int):
        self.hours, self.minutes, self.seconds = hours, minutes, seconds

    @GObject.Property(type=object)
    def timer_clock(self) -> TimerClock:
        return TimerClock(self.hours, self.minutes, self.seconds)
    
    @GObject.Property(type=object)
    def alarm_clock(self) -> AlarmClock:
        return AlarmClock(self.hours, self.minutes, self.seconds)

    @timer_clock.setter
    def set_timer_clock(self, value: TimerClock):
        self.hours, self.minutes, self.seconds = value.get_hours_minutes_and_seconds()

    @alarm_clock.setter
    def set_alarm_clock(self, value: AlarmClock):
        self.hours, self.minutes, self.seconds = value.get_hours_minutes_and_seconds()
