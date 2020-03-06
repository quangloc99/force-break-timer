import gi
from gi.repository import GObject


# This is just a simple "polyfill" for GObject.Object#bind_property_full
# somehow they make this method "unsupported". But this method is 
# so usefull, I decided to make one.
# TODO: another functionallity like unbind
class FullPropertyBinder(GObject.Object):
    def __init__(self, 
        source_obj, src_prop_name, dest_obj, dest_prop_name, flag, 
        source_to_dest = None,
        dest_to_source = None
    ):
        super().__init__()
        self.source_obj = source_obj
        self.dest_obj = dest_obj
        self.source_prop_name = src_prop_name
        self.dest_prop_name = dest_prop_name
        self.source_to_dest = source_to_dest
        self.dest_to_source = dest_to_source
        self.flag = flag
        self._do_bind()

    def _do_bind(self):
        self.source_obj.connect('notify::' + self.source_prop_name, self._on_source_change)
        if self.flag == GObject.BindingFlags.BIDIRECTIONAL:
            print('bound dest change')
            self.dest_obj.connect('notify::' + self.dest_prop_name, self._on_dest_change)

        if self.flag in [GObject.BindingFlags.SYNC_CREATE, GObject.BindingFlags.BIDIRECTIONAL]:
            self._on_source_change()

    def _on_source_change(self, *args, **kwargs):
        value = self.source_to_dest(self.source_obj.get_property(self.source_prop_name))
        if value != self.dest_obj.get_property(self.dest_prop_name): 
            self.dest_obj.set_property(self.dest_prop_name, value)

    def _on_dest_change(self, *args, **kwargs):
        value = self.dest_to_source(self.dest_obj.get_property(self.dest_prop_name))
        if value != self.source_obj.get_property(self.source_prop_name): 
            self.source_obj.set_property(self.source_prop_name, value)

def bind_property_full(
        source_obj, src_prop_name, dest_obj, dest_prop_name, flag, 
        source_to_dest = None,
        dest_to_source = None
    ):
    try:
        GObject.Object.bind_property_full(source_obj, src_prop_name, dest_obj, dest_prop_name,
                source_to_dest, dest_to_source)
    except RuntimeError:
        return FullPropertyBinder(
            source_obj, src_prop_name, dest_obj, dest_prop_name, flag, 
            source_to_dest, dest_to_source
        )
