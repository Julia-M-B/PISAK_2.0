import copy

from PySide6.QtGui import QFocusEvent
from PySide6.QtWidgets import QWidget

from pisak.utils import get_id


class PisakScannableItem:

    def __init__(self, *args, **kwargs):
        self._id = get_id()
        self._items = []
        self._scannable_items = []
        # self._scanning_runner = None
        self._scanning_strategy = None
        self._loops_counter = 0

    def __str__(self):
        return f"{self.__class__.__name__} id={self._id}"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        self._iter_items = iter(self._scannable_items)
        return self

    def __next__(self):
        try:
            item = next(self._iter_items)
            print("Next item", item)
            self._loops_counter += 1
            return item
        except StopIteration:
            print("Recurrent next call")
            return next(iter(self))

    @property
    def items(self):
        return copy.copy(self._items)

    @property
    def scannable_items(self):
        return copy.copy(self._scannable_items)

    @property
    def scanning_strategy(self):
        return self._scanning_strategy

    @property
    def loops_counter(self):
        return self._loops_counter

    @loops_counter.setter
    def loops_counter(self, val):
        self._loops_counter = val

    def add_item(self, item):
        raise NotImplementedError("Method add_item is not implemented.")

    def add_scannable_items(self):
        raise NotImplementedError("Method add_scannable_item is not implemented.")

    def init_ui(self):
        raise NotImplementedError("Method init_ui is not implemented.")

    def set_layout(self):
        raise NotImplementedError("Method set_layout is not implemented.")

    def highlight_all(self):
        raise NotImplementedError("Method highlight_all is not implemented.")

    def reset_highlight_all(self):
        raise NotImplementedError("Method reset_highlight_all is not implemented.")


class PisakScannableWidget(QWidget, PisakScannableItem):

    def __init__(self, parent):
        super().__init__(parent)

    def add_item(self, item):
        # if not isinstance(item, PisakScannableItem):
            # raise ValueError("Item should be PisakScannableItem.")
        # if isinstance(item, PisakScannableItem):
        self._items.append(item)
        if isinstance(item, PisakScannableItem):
            self._scannable_items.append(item)

    def highlight_all(self):
        for item in self._scannable_items:
            item.highlight_all()

    def reset_highlight_all(self):
        for item in self._scannable_items:
            item.reset_highlight_all()

    def focusInEvent(self, event: QFocusEvent):
        if event.gotFocus():
            self.highlight_all()
        else:
            super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        if event.lostFocus():
            self.reset_highlight_all()
        else:
            super().focusOutEvent(event)



