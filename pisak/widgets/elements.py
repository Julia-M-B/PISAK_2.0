from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QFocusEvent, QKeyEvent, QFont
from PySide6.QtWidgets import QPushButton, QLabel

from pisak.scanning.scannable import PisakScannableItem
from pisak.scanning.strategies import BackToParentStrategy, Strategy


class PisakButton(QPushButton, PisakScannableItem):

    send_text_signal = Signal(QPushButton)

    def __init__(
        self,
        parent,
        text: str = "",
        scanning_strategy: Strategy = BackToParentStrategy(),
    ):
        super().__init__(parent=parent, text=text)
        self._scanning_strategy = scanning_strategy
        self._text = text

        self.init_ui()
        self.clicked.connect(self.button_clicked)

    def init_ui(self):
        self.setFont(QFont("Arial", 16))
        self.setStyleSheet("""
                            background-color: #ede4da;
                            color: black;
                            border-style: solid;
                            border-width: 2px;
                            border-color: black;
                            border-radius: 5px;
                            min-height: 50px;
                            font-weight: bold;
                            """)

    @property
    def text(self):
        return self._text

    # test slot
    @Slot()
    def button_clicked(self) -> None:
        print(f"Button {str(self)} was clicked!")
        self.send_text_signal.emit(self)

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
        self.setStyleSheet("""
                            background-color: #5ea9eb;
                            color: black;
                            border-style: solid;
                            border-width: 2px;
                            border-color: #9dccf5;
                            border-radius: 5px;
                            min-height: 50px;
                            font-weight: bold;
                            """)

    def reset_highlight_self(self):
        self.init_ui()

    def highlight_all(self):
        self.highlight_self()

    def reset_highlight_all(self):
        self.reset_highlight_self()

    def keyPressEvent(self, event: QKeyEvent):
        # przechwytywanie wciśnięcia 1,
        # gdy jest focus na przycisku
        if self.hasFocus() and event.key() == Qt.Key_1:
            # zatrzymujemy skanujący worker w widgecie-rodzicu
            # self.parentWidget()._scanning_worker.stop()
            self.parentWidget().timer.stop()
            # symulujemy kliknięcie na przycisk
            self.click()
            # wywołujemy metodę skan na widgecie dwa poziomy wyżej?
            self.parentWidget().parentWidget().scan()
            return
        super().keyPressEvent(event)


class PisakDisplay(QLabel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.init_ui()

    def init_ui(self):
        self.setFont(QFont("Arial", 16))
        self.setAlignment(Qt.AlignVCenter)
        self.setLineWidth(10)
        self.setStyleSheet("""
                            background-color: #f0f0f0;
                            color: black;
                            border-style: solid;
                            border-width: 2px;
                            border-color: black;
                            border-radius: 5px;
                            padding: 5px;
                            margin-bottom: 10px;
                            """)

