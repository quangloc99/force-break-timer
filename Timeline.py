import gi
from gi.repository import GLib, GObject
from typing import *

class Timeline(GObject.Object):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "stopped": (GObject.SignalFlags.RUN_FIRST, None, ())
    }
    def __init__(self, timeline: List[Tuple[int, Callable[[], bool]]]):
        super().__init__()
        self.__timeline_iter = iter(timeline)
        self.__started = False
        self.__stopped = False
        self.__cur_elm = None
        self.__timeout_id = -1

    def start(self):
        if self.__started:
            return 
        self.__started = True
        self.__set_timeout_next()

    def stop(self):
        if self.__stopped:
            return
        if self.__timeout_id != -1:
            GLib.source_remove(self.__timeout_id)

        self.__stopped = True
        self.emit("stopped")

    def __set_timeout_next(self):
        try:
            self.__cur_elm = next(self.__timeline_iter)
            duration = self.__cur_elm[0]
            self.__timeout_id = GLib.timeout_add(duration, self.__timeout_callback)
        except StopIteration:
            self.stop()

    def __timeout_callback(self):
        self.__timeout_id = -1
        if self.__stopped:
            return 
        cb = self.__cur_elm[1]
        ret = cb()
        if ret is not None and not ret:
            self.stop()
            return False
        self.__set_timeout_next()
        return False


