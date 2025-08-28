from string import ascii_uppercase, ascii_lowercase

from pisak.widgets.containers import PisakColumnWidget, PisakRowWidget
from pisak.widgets.elements import PisakButtonBuilder
from pisak.scanning.scannable import PisakScannableWidget


class Keyboard(PisakColumnWidget, PisakScannableWidget):
    def __init__(self, parent=None, keyboard_layout=None, keyboard_dim=(4, 7)):
        super().__init__(parent)
        self._keyboard_layout = keyboard_layout
        self._keyboard_dim = keyboard_dim
        self._buttons = []
        self._implement_layout()

    # TODO chociaż rozwiązanie ze statecznymi metodami jest mega ładne i zwięzłe
    #  to chyba lepiej zmienić to tak, aby konfiguracja danego keyboardu była
    #  implementowana z zewnętrznych konfigów w postaci słowników/jsonów ??
    #  Bo dla samych liter/cyfer, to jest to bardzo ładne i proste, ale co ze
    #  wszystkimi dodatkowymi guzikami, typu strzałki, spacja,
    #  znaki interpunkcyjne, etc. ??? Też chyba nie powinno być tak, że
    #  przyciski specjalne są na sztywno przypisane do jednej klawiatury, że np.
    #  na sztywno ustalone jest, że przecinek, kropka i wykrzyknik umieszczone
    #  są w klawiaturze z dużymi literami, a znak zapytania, średnik i nawiasy
    #  w klawiaturze z małymi literami

    @staticmethod
    def alphabetical_upper(parent):
        """
        Metoda tworzy i zwraca obiekt typu 'Keyboard' z literowymi przyciskami
        :param: parent — rodzic utworzonej klawiatury
        """
        keyboard_dim = (4, 7)
        horizontal_size = keyboard_dim[1]
        characters = ascii_uppercase
        num_of_letters = len(characters)
        keyboard_layout = [
            list(characters[i : i + horizontal_size])
            for i in range(0, num_of_letters + 1, horizontal_size)
        ]
        return Keyboard(
            parent=parent, keyboard_layout=keyboard_layout, keyboard_dim=keyboard_dim
        )

    @staticmethod
    def alphabetical_lower(parent):
        """
        Metoda tworzy i zwraca obiekt typu 'Keyboard' z literowymi przyciskami
        :param: parent — rodzic utworzonej klawiatury
        """
        keyboard_dim = (4, 7)
        horizontal_size = keyboard_dim[1]
        characters = ascii_lowercase
        num_of_letters = len(characters)
        keyboard_layout = [
            list(characters[i: i + horizontal_size])
            for i in range(0, num_of_letters + 1, horizontal_size)
        ]
        return Keyboard(
            parent=parent, keyboard_layout=keyboard_layout,
            keyboard_dim=keyboard_dim
        )

    @staticmethod
    def numerical(parent):
        """
        Metoda tworzy i zwraca obiekt typu 'Keyboard' z numerycznymi przyciskami
        :param: parent — rodzic utworzonej klawiatury
        """
        keyboard_dim = (4, 3)
        horizontal_size = keyboard_dim[1]
        list_of_numbers = [x for x in range(9, -1, -1)]
        keyboard_layout = [
            sorted(list_of_numbers[i : i + horizontal_size])
            for i in range(0, len(list_of_numbers) + 1, horizontal_size)
        ]
        return Keyboard(
            parent=parent, keyboard_layout=keyboard_layout, keyboard_dim=keyboard_dim
        )

    def _implement_layout(self):
        for row in self._keyboard_layout:
            row_widget = PisakRowWidget(parent=self)
            for letter in row:
                button = PisakButtonBuilder().set_text(str(letter)).emit_text_signal(str(letter)).build(row_widget)
                row_widget.add_item(button)
                self._buttons.append(button)
            row_widget.set_layout()
            self.add_item(row_widget)
        self.set_layout()

    @property
    def buttons(self):
        return self._buttons


