from string import ascii_lowercase

from pisak.widgets.elements import PisakButton
from pisak.widgets.containers import PisakRowWidget, PisakColumnWidget
from pisak.widgets.scannable import PisakScannableWidget


class Keyboard(PisakRowWidget, PisakScannableWidget):
    def __init__(self, parent=None, keyboard_layout=None, keyboard_dim=(4, 7)):
        super().__init__(parent)
        self._keyboard_layout = keyboard_layout
        self._keyboard_dim = keyboard_dim
        self._implement_layout()

    @staticmethod
    def alphabetical(parent):
        """
        Metoda tworzy i zwraca obiekt typu 'Keyboard' z literowymi przyciskami
        :param: parent — rodzic utworzonej klawiatury
        """
        keyboard_dim = (4, 7)
        horizontal_size = keyboard_dim[1]
        num_of_letters = len(ascii_lowercase)
        keyboard_layout = [
            list(ascii_lowercase[i : i + horizontal_size])
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
            row_widget = PisakColumnWidget(parent=self)
            for letter in row:
                button = PisakButton(parent=row_widget, label=str(letter))
                row_widget.add_item(button)
            row_widget.set_layout()
            self.add_item(row_widget)
        self.set_layout()
