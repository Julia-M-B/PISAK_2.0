from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow, QSizePolicy, QStackedWidget
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, Signal

from pisak.scanning.manager import ScannableManagerMeta
from pisak.widgets.containers import PisakGridWidget
from pisak.scanning.scannable import PisakScannableItem
from pisak.scanning.strategies import TopStrategy


class PisakBaseModule(QMainWindow, metaclass=ScannableManagerMeta):
    start_scanning_signal = Signal(QObject)
    key_pressed_signal = Signal()

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

    def show(self):
        super().show()
        self.setFocus()

    def closeEvent(self, event):
        self.parent().closeEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        # gdy nic nie jest skanowane, to po wciśnięciu przycisku
        # ma się rozpocząć skanowanie
        if event.key() == Qt.Key_1:
            if not self.focusWidget() or self.hasFocus():
                # TODO gdy mamy tylko jeden element w kontenerze najbardziej zewnętrznym,
                #  czyli w PisakGridWidget, to od razu skanować elementy-dzieći (wiersze
                #  lub kolumny) tego jedynego elementu siedzącego w Gridzie;
                #  bo teraz skanowanie zaczyna się od skanowania elementów Grida, czyli tak
                #  naprawdę x razy pod rząd podświetlamy ten sam element, bez przerw między
                #  podświetleniami
                if len(self.centralWidget().scannable_items) == 1:
                    self.start_scanning_signal.emit(self.centralWidget().scannable_items[0])
                else:
                    self.start_scanning_signal.emit(self.centralWidget())
            else:
                self.key_pressed_signal.emit()
        super().keyPressEvent(event)

