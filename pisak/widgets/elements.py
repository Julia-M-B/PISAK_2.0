from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QFocusEvent, QKeyEvent
from PySide6.QtWidgets import QPushButton

from pisak.widgets.scannable import PisakScannableItem
from pisak.widgets.strategies import BackToParentStrategy, Strategy


class PisakButton(QPushButton, PisakScannableItem):

    def __init__(
        self,
        parent,
        text: str = "",
        scanning_strategy: Strategy = BackToParentStrategy(),
    ):
        super().__init__(parent=parent, text=text)
        self._scanning_strategy = scanning_strategy

        self.init_ui()
        self.clicked.connect(self.button_clicked)

    def init_ui(self):
        self.setStyleSheet("background-color: blue;")

    # test slot
    @Slot()
    def button_clicked(self) -> None:
        print(f"Button {str(self)} was clicked!")

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

    def stop_scanning(self):
        self._scanning_worker.stop()
        print("Stoping scanning worker")

    def reset_scan(self):
        self.stop_scanning()
        self._scanning_strategy.reset_scan(self)

    def highlight_self(self):
        self.setStyleSheet("background-color: green;")

    def reset_highlight_self(self):
        self.setStyleSheet("background-color: blue;")

    def highlight_all(self):
        self.highlight_self()

    def reset_highlight_all(self):
        self.reset_highlight_self()

    def keyPressEvent(self, event: QKeyEvent):
        # przechwytywanie wciśnięcia 1,
        # gdy jest focus na przycisku
        if self.hasFocus() and event.key() == Qt.Key_1:
            # zatrzymujemy skanujący worker w widgecie-rodzicu
            self.parentWidget()._scanning_worker.stop()
            # symulujemy kliknięcie na przycisk
            self.click()
            # wywołujemy metodę skan na widgecie dwa poziomy wyżej?
            self.parentWidget().parentWidget().scan()
            return
        super().keyPressEvent(event)
