import gi
from gi.repository import GLib, GObject
from typing import *

TimelineList = Iterable[Union[int, Callable[..., bool]]]

class Timeline(GObject.Object):
    __gsignals__: Dict[str, Tuple[Any, Any, Any]] = {
            "stopped": (GObject.SignalFlags.RUN_FIRST, None, ())
    }
    def __init__(self, timeline: TimelineList):
        super().__init__()
        self.__timeline = list(timeline)
        self.__iter = self.__timeline_iter()
        self.__started = False
        self.__stopped = False
        self.__cur_elm = None
        self.__timeout_id = -1

    def start(self):
        if self.__started:
            return 
        self.__started = True
        self.__run_next()

    def stop(self):
        if self.__stopped:
            return
        if self.__timeout_id != -1:
            GLib.source_remove(self.__timeout_id)

        self.__stopped = True
        self.emit("stopped")

    def __timeline_iter(self):
        for i in self.__timeline:
            if self.__stopped:
                return 
            if type(i) == int:
                self.__timeout_id = GLib.timeout_add(i, self.__run_next)
                yield
            else:
                res = i()
                if res is not None and not res:
                    self.stop()
                    break

    def __run_next(self):
        self.__timeout_id = -1
        if self.__stopped:
            return False
        try:
            next(self.__iter)
            return False
        except StopIteration:
            return False



