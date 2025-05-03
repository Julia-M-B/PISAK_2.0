from PySide6.QtWidgets import QWidget

from pisak.apps.base_app import PisakBaseApp
from pisak.components.keyboard import Keyboard
from pisak.widgets.scannable import PisakScannableWidget


# @Singleton
class PisakSpellerApp(PisakBaseApp):
    """
    Moduł Speller aplikacji Pisak.
    """

    def __init__(self, parent=None):
        """
        :param QWidget parent: obiekt-rodzic modułu Speller
        """
        super().__init__(parent=parent, title="Speller")
        self._keyboard = Keyboard.alphabetical(parent=self.centralWidget())
        self.centralWidget().add_item(self._keyboard)

        self.init_ui()

    def init_ui(self):
        super().init_ui()
        self.centralWidget().layout.addWidget(self._keyboard)
        self.centralWidget().set_layout()
