from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QLayout


from pisak.scanning.scannable import PisakScannableWidget
from pisak.scanning.strategies import BackToParentStrategy, Strategy


class PisakContainerWidget(PisakScannableWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent)
        self._scanning_strategy = strategy
        self._layout: Optional[QLayout] = None

    @property
    def layout(self):
        return self._layout

    def set_layout(self) -> None:
        for item in self._items:
            self._layout.addWidget(item)
        self.setLayout(self._layout)

    def init_ui(self):
        self.setFocusPolicy(Qt.StrongFocus)


class PisakGridWidget(PisakContainerWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent, strategy)
        self._layout = QGridLayout()


class PisakColumnWidget(PisakContainerWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent, strategy)
        self._layout = QVBoxLayout()


class PisakRowWidget(PisakContainerWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent, strategy)
        self._layout = QHBoxLayout()

