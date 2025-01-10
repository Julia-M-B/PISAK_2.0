from PySide6.QtGui import QFocusEvent
from PySide6.QtWidgets import QLabel, QPushButton

from pisak.widgets.scannable import PisakScannableItem
from pisak.widgets.strategies import BackToParentStrategy


class PisakButton(QPushButton, PisakScannableItem):
    def __init__(self, parent, text=""):
        super().__init__(parent=parent, text=text)
        self._strategy = BackToParentStrategy()
        self.init_ui()


    def init_ui(self):
        self.setStyleSheet("background-color: blue;")
        # self.setFocusPolicy(Qt.StrongFocus)


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

    def highlight_self(self):
        # print(self, "highlight_self")
        self.setStyleSheet("background-color: green;")

    def reset_highlight_self(self):
        # print(self, "reset_highlight_self")
        self.setStyleSheet("background-color: blue;")

    def highlight_all(self):
        self.highlight_self()

    def reset_highlight_all(self):
        self.reset_highlight_self()

