from PySide6.QtWidgets import QMainWindow, QSizePolicy

from pisak.widgets.strategies import TopStrategy


class PisakBaseApp(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self._strategy = TopStrategy()
        self._items = []
        self._central_widget = PisakGridWidgets(self)
        self.setCentralWidget(self._central_widget)

    def init_ui(self):
        self._central_widget.setGeometry(0, 0, self.height(), self.width())
        self._central_widget.setSizePolicy(QSizePolicy.Expanding,
                                           QSizePolicy.Expanding)
        self._central_widget.show()

    # def scan(self):
    #     return NotImplemented
    #
    # def show(self):
    #     super().show()
        # self.scan()