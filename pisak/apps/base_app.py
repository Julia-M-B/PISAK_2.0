import copy

from PySide6.QtWidgets import QMainWindow, QSizePolicy, QStackedWidget

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

    def init_ui(self):
        self.setWindowTitle(self._title)
        self.setGeometry(0, 0, 600, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._central_widget.setGeometry(0, 0, self.height(), self.width())
        self._central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._central_widget.show()

    def scan(self):
        self.centralWidget().scan()

    def show(self):
        super().show()
        self.scan()

    def stop_scanning(self):
        pass

    def closeEvent(self, event):
        self.parent().closeEvent(event)


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
