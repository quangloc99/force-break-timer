import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ForceBreakIndicatorMenu(Gtk.Menu):
    def __init__(self):
        super().__init__()
