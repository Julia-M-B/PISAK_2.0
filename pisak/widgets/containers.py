from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout

from pisak.widgets.scannable import PisakScannableWidget
from pisak.widgets.strategies import Strategy, BackToParentStrategy


class PisakGridWidget(PisakScannableWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent)
        self._strategy = strategy
        self._layout = QGridLayout()

    def set_layout(self) -> None:
        for item in self._items:
            self._layout.addWidget(item)
        self.setLayout(self._layout)

    def init_ui(self):
        self.setFocusPolicy(Qt.StrongFocus)

class PisakRowWidget(PisakScannableWidget):
    pass


class PisakColumnWidget(PisakScannableWidget):
    pass