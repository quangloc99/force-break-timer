import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, GLib, GObject, AppIndicator3

from typing import *
from datetime import datetime

from Clock import TimerClock
from ForceBreakIndicatorMenu import ForceBreakIndicatorMenu
from AppWindow import AppWindow

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

# TODO: AppIndicator some how throw the following assertion:
#
#      gdk_window_thaw_toplevel_updates: assertion 'window->update_and_descendants_freeze_count > 0' failed
#
# The app is somehow working fine, but this bother me. And because of that this is TODO but not FIXME.
class App:
    def __init__(self):
        self.win = AppWindow(now = self.get_now())
        self.indicator_menu = ForceBreakIndicatorMenu(now = self.get_now())
        self.indicator = AppIndicator3.Indicator.new(
                "com.github.quangloc99.force_break",
                "system-run",       # this is just a placeholder
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )

        self.connect_signals()
        self.show()

    def connect_signals(self):
        self.win.connect('quit', self.ask_quit)
        self.indicator_menu.connect('quit-activated', self.ask_quit)
        self.indicator_menu.connect('focus', self.show_indicator_menu)

    def show_indicator_menu(self, *args):
        self.indicator_menu.set_now(self.get_now())

    def show(self):
        self.win.show_all()
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.indicator_menu) 

    def ask_quit(self, parent, *args):
        print(parent, args)
        dialog = Gtk.Dialog(parent = parent if isinstance(parent, Gtk.Window) else None)
        dialog.get_content_area().set_center_widget(
            Gtk.Label(label="Do you really want to quit?", margin=10)
        )
        dialog.add_button("Yes", 1)
        dialog.add_button("No", 2)
        dialog.set_default_response(2)
        def yes_quit(_, id):
            if id == 1:
                Gtk.main_quit()
            else:
                dialog.close()
        dialog.connect('response', yes_quit)
        dialog.show_all()
        dialog.run()

    def get_now(self):
        return datetime.now()

if __name__ == "__main__":
    app = App()
    app.indicator_menu.set_clock(TimerClock()) 
    Gtk.main()

