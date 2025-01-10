import copy

from PySide6.QtWidgets import QWidget

from pisak.utils import get_id

class PisakScannableItem:
    def __init__(self, *args, **kwargs):
        self._id = get_id()

    def __str__(self):
        return f"{self.__class__.__name__} id={self._id}"

    def __repr__(self):
        return self.__str__()

class PisakScannableWidget(QWidget, PisakScannableItem):
    def __init__(self, parent):
        super().__init__(parent)
        self._items = []

    @property
    def items(self):
        # print(self._items)
        return copy.copy(self._items)

    def add_item(self, item):
        if not isinstance(item, PisakScannableItem):
            raise ValueError("Item should be PisakScannableItem.")
        self._items.append(item)

    def init_ui(self):
        return NotImplemented

