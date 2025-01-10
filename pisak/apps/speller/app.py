from PySide6.QtWidgets import QWidget

from pisak.apps.base_app import PisakBaseApp
from pisak.components.keyboard import Keyboard


# @Singleton
class PisakSpellerApp(PisakBaseApp):
    """
    Moduł Speller aplikacji Pisak.
    """
    def __init__(self, parent: QWidget):
        """
        :param QWidget parent: obiekt-rodzic modułu Speller
        """
        super().__init__(parent)
        self._keyboard = Keyboard.alphabetical(self.centralWidget())