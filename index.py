import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk, GLib, GObject, AppIndicator3, Notify

from typing import *
from datetime import datetime, timedelta
from functools import partial

from AppState import AppState
from Clock import TimerClock, AlarmClock
from ForceBreakIndicatorMenu import ForceBreakIndicatorMenu
from AppWindow import AppWindow
from Timeline import Timeline
from enum import *

APP_NAME = "com.github.quangloc99.force_break"

css = b"""
    .header {
        font-size: 30px;
    }
"""

def main():
    css_provider= Gtk.CssProvider()
    css_provider.load_from_data(css)
    Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    Notify.init(APP_NAME)

    app = App()
    app.show_indicator()
    app.state.picked_clock = TimerClock(minutes=25)
    app.pick_new_clock()
    app.update_now_periodically(500)
    Gtk.main()
    
def finalize():
    Notify.uninit()
    Gtk.main_quit()

# TODO: AppIndicator some how throw the following assertion:
#
#      gdk_window_thaw_toplevel_updates: assertion 'window->update_and_descendants_freeze_count > 0' failed
#
# The app is somehow working fine, but this bother me. And because of that this is TODO but not FIXME.
class UI_STATE(Enum):
    PICKING_CLOCK = auto()
    RUNNING_CLOCK = auto()

class App:
    def __init__(self):
        self.state = AppState()
        self.ui_state = None
        self.indicator_menu = ForceBreakIndicatorMenu()
        self.indicator = AppIndicator3.Indicator.new(
                APP_NAME,
                "system-run",       # this is just a placeholder
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.binds_indicator_menu_state(self.indicator_menu)
        self.alarm_timeline = None
        self.__countdown_notify = Notify.Notification.new("")

    def update_now_periodically(self, interval_ms: int = 500):
        def timeout_callback():
            self.state.reset_now()
            return True
        return GLib.timeout_add(interval_ms, timeout_callback)

    def new_app_window(self):
        win = AppWindow()
        self.binds_window_state(win)
        return win

    def binds_indicator_menu_state(self, indicator_menu):
        self.state.bind_property('now', indicator_menu, 'now', GObject.BindingFlags.SYNC_CREATE)
        self.state.bind_property('running_clock', indicator_menu, 'running_clock', GObject.BindingFlags.SYNC_CREATE)

        indicator_menu.connect('reset-clock-activated', self.pick_new_clock)
        indicator_menu.connect('quit-activated', self.ask_quit)

    def binds_window_state(self, window):
        self.state.bind_property('picked_clock', window, 'picking_clock', GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE)
        self.state.bind_property('now', window, 'now', GObject.BindingFlags.SYNC_CREATE)

        window.connect('quit', self.ask_quit)
        window.connect('clock-picked', self.reset_running_clock)
        window.connect('clock-picked', lambda *args: window.close())

    def reset_running_clock(self, *args):
        if self.ui_state == UI_STATE.RUNNING_CLOCK:
            return 
        self.ui_state = UI_STATE.RUNNING_CLOCK
        self.state.reset_running_clock()
        clock = self.state.running_clock.to_timer_clock(self.state.now)
        self.alarm_timeline = Timeline(self.generate_alarm_timeline(clock.duration))
        self.alarm_timeline.start()

    def pick_new_clock(self, *args):
        if self.ui_state == UI_STATE.PICKING_CLOCK:
            return 
        self.ui_state = UI_STATE.PICKING_CLOCK
        self.state.remove_running_clock()
        win = self.new_app_window()
        win.show_all()
        win.fullscreen() 
        win.present()
        if self.alarm_timeline is not None:
            self.alarm_timeline.stop()

    def show_indicator(self):
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.indicator_menu) 

    def generate_alarm_timeline(self, duration: timedelta):
        res = []
        res.append(self.pick_new_clock)
        one_sec = timedelta(seconds=1)

        for countdown in range(1, 4):
            if duration < one_sec:
                break
            duration -= one_sec
            res.append(1000)
            res.append(partial(self.reset_and_show_countdown_notify, "Timer ends in " + str(countdown)))
        res.append(int(duration.total_seconds() * 1000))
        return reversed(res)
        
    def reset_and_show_countdown_notify(self, summary):
        self.__countdown_notify.update(summary)
        self.__countdown_notify.show()

    def ask_quit(self, parent, *args):
        dialog = Gtk.Dialog(parent = parent if isinstance(parent, Gtk.Window) else None)
        dialog.get_content_area().set_center_widget(
            Gtk.Label(label="Do you really want to quit?", margin=10)
        )
        dialog.add_button("Yes", 1)
        dialog.add_button("No", 2)
        dialog.set_default_response(2)
        dialog.show_all()
        if dialog.run() == 1:
            finalize()
        else:
            dialog.close()

if __name__ == "__main__":
    main()
