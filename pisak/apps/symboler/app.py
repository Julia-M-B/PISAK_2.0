from pisak.apps.base_app import PisakBaseApp
from pisak.components.keyboard import Keyboard


class PisakSymbolerApp(PisakBaseApp):
    def __init__(self, parent=None):
        super().__init__(parent, title="Symboler")
        self._keyboard = Keyboard.numerical(self.centralWidget())
        self.centralWidget().add_item(self._keyboard)

        self.init_ui()

    def init_ui(self):
        super().init_ui()
        self.centralWidget().layout.addWidget(self._keyboard)
        self.centralWidget().set_layout()
