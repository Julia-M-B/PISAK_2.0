import copy

from PySide6.QtWidgets import QMainWindow, QSizePolicy, QStackedWidget
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt

from pisak.widgets.containers import PisakGridWidget
from pisak.widgets.scannable import PisakScannableItem, PisakScannableWidget
from pisak.widgets.strategies import TopStrategy


class PisakBaseApp(QMainWindow):
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self._strategy = TopStrategy()
        self._title = title
        self._items = []
        self._central_widget = PisakGridWidget(parent=self)
        self.setCentralWidget(self._central_widget)

    def __str__(self):
        return f"{self.__class__.__name__} name={self._title}"

    def __repr__(self):
        return self.__str__()

    def init_ui(self):
        self.setWindowTitle(self._title)
        self.setGeometry(0, 0, 600, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._central_widget.setGeometry(0, 0, self.height(), self.width())
        self._central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._central_widget.show()
        self.setStyleSheet("""
                            background-color: #d9cfc5;
                            """)

    def scan(self):
        self.centralWidget().scan()

    def show(self):
        super().show()
        self.scan()

    def stop_scanning(self):
        print(f"Stopping scanning {self} app")
        focused_widget = self.focusWidget()
        if focused_widget:
            focused_widget.parent().stop_scanning()

    def closeEvent(self, event):
        self.parent().closeEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        # gdy nic nie jest skanowane, to po wciśnięciu przycisku
        # ma się rozpocząć skanowanie
        if not self.focusWidget() and event.key() == Qt.Key_1:
            self.scan()
        super().keyPressEvent(event)


class PisakAppsWidget(QStackedWidget, PisakScannableItem):
    """
    klasa do przechowywania ikonek różnych modułów w głównym menu
    singleton??
    """

    def __init__(self, parent):
        super().__init__(parent)
        # self._items = []

    # @property
    # def items(self):
    #     return copy.copy(self._items)

    def add_item(self, item):
        if not isinstance(item, PisakBaseApp):
            raise ValueError("Item should be PisakBaseApp.")
        self._items.append(item)

    def init_ui(self):
        return NotImplemented

    def set_layout(self):
        return NotImplemented

    def switch_to_window(self, new_window: PisakBaseApp):
        old_window = self.currentWidget()
        if old_window:
            old_window.stop_scanning()
        self.setCurrentWidget(new_window)
        new_window.show()

