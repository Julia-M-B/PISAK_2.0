from string import ascii_uppercase

from pisak.widgets.containers import PisakColumnWidget, PisakRowWidget
from pisak.widgets.elements import PisakButton
from pisak.widgets.scannable import PisakScannableWidget


class Keyboard(PisakColumnWidget, PisakScannableWidget):
    def __init__(self, parent=None, keyboard_layout=None, keyboard_dim=(4, 7)):
        super().__init__(parent)
        self._keyboard_layout = keyboard_layout
        self._keyboard_dim = keyboard_dim
        self._buttons = []
        self._implement_layout()

    @staticmethod
    def alphabetical(parent):
        """
        Metoda tworzy i zwraca obiekt typu 'Keyboard' z literowymi przyciskami
        :param: parent — rodzic utworzonej klawiatury
        """
        keyboard_dim = (4, 7)
        horizontal_size = keyboard_dim[1]
        characters = ascii_uppercase + " "
        num_of_letters = len(characters)
        keyboard_layout = [
            list(characters[i : i + horizontal_size])
            for i in range(0, num_of_letters + 1, horizontal_size)
        ]
        return Keyboard(
            parent=parent, keyboard_layout=keyboard_layout, keyboard_dim=keyboard_dim
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
                button = PisakButton(parent=row_widget, text=str(letter))
                row_widget.add_item(button)
                self._buttons.append(button)
            row_widget.set_layout()
            self.add_item(row_widget)
        self.set_layout()

    @property
    def buttons(self):
        return self._buttons
