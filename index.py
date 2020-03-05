import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, GLib, GObject, AppIndicator3
from typing import *

from Clock import ClockType
from NotifyClockPickerWidget import NotifyClockPickerWidget
from ForceBreakIndicatorMenu import ForceBreakIndicatorMenu

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
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "quit": (GObject.SignalFlags.RUN_FIRST, None, tuple())
    }

    def __init__(self, **kwargs):
        super().__init__(title="Force break", **kwargs)

        self._clock_picker = NotifyClockPickerWidget()
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

# TODO: AppIndicator some how throw the following assertion:
# gdk_window_thaw_toplevel_updates: assertion 'window->update_and_descendants_freeze_count > 0' failed
# The app is somehow working fine, but this bother me. And because of that this is TODO but not FIXME.
class App:
    def __init__(self):
        self.win = AppWindow()
        self.indicator_menu = ForceBreakIndicatorMenu()
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

if __name__ == "__main__":
    app = App()
    app.win.fullscreen() 
    Gtk.main()

