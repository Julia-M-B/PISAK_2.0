from PySide6.QtWidgets import QWidget

from pisak.modules.base_module import PisakBaseModule
from pisak.components.keyboard import Keyboard
from pisak.widgets.elements import PisakDisplay

"""
Funkcjonalności spellerowej klawiatury:
powinny być dwie "wymienne" klawiatury, tak jak w telefonie, na litery i na pozostałe znaki?
Domyślna klawiatura:
- wszystkie litery -> kliknięcie na przycisk z literą powinno "wyświetlać" daną literę
- spacja -> dodaje spację 
- backspace -> usuwa ostatni znak
- enter -> dodaje nową linię
- znak do wyjścia ze skanowania danej grupy elementów i skanowania rodzica
- znaki interpunkcyjne: kropka, przecinek


Druga klawiatura: 
- wszystkie cyfry -> analogicznie do liter
- spacja -> dodaje spację 
- backspace -> usuwa ostatni znak
- enter -> dodaje nową linię
- znak do wyjścia ze skanowania danej grupy elementów i skanowania rodzica
- znaki specjalne: znak zapytania, wykrzyknik, procent, etc ??

Niezależnie od klawiatur w jakiejś linijce na górze powinny wyświetlać się predykcje ??

Możliwość kliknięcia opcji "czytaj" ???

Czy powinny być dostępne strzałki? Chyba tak

"""

# @Singleton
class PisakSpellerModule(PisakBaseModule):
    """
    Moduł Speller aplikacji Pisak.
    """

    def __init__(self, parent=None):
        """
        :param QWidget parent: obiekt-rodzic modułu Speller
        """
        super().__init__(parent=parent, title="Speller")
        self._display = PisakDisplay(parent=self.centralWidget())
        self._keyboard = Keyboard.alphabetical(parent=self.centralWidget())
        self.centralWidget().add_item(self._display)
        self.centralWidget().add_item(self._keyboard)

        for button in self._keyboard.buttons:
            button.send_text_signal.connect(self.display_text)

        self.init_ui()

    def init_ui(self):
        super().init_ui()
        # self.centralWidget().layout.addWidget(self._display, 0, 0)
        # self.centralWidget().layout.addWidget(self._keyboard, 1, 0)
        self.centralWidget().set_layout()

    def display_text(self, button):
        print(1111)
        self._display.setText(self._display.text() + button.text)

