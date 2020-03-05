import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from typing import Dict, Tuple, Any

class ForceBreakIndicatorMenu(Gtk.Menu):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "quit-activated": (GObject.SignalFlags.RUN_FIRST, None, tuple())
    }
    def __init__(self):
        super().__init__()
        self._quit_item = Gtk.MenuItem(label="Quit")
        self.add(self._quit_item)

        self._connect_signals()
        self.show_all()

    def _connect_signals(self):
        self._quit_item.connect("activate", self._on_quit)

    def _on_quit(self, widget):
        self.emit("quit-activated")
