from typing import Optional, Callable

from PySide6.QtCore import QObject
from PySide6.QtCore import Slot, Qt, Signal, QTimer
from PySide6.QtGui import QFocusEvent, QFont, QPainter, QFontMetrics, QPen, \
    QIcon
from PySide6.QtWidgets import QPushButton, QLabel, QStackedWidget

from pisak.scanning.scannable import PisakScannableItem
from pisak.scanning.strategies import BackToParentStrategy, Strategy

class PisakStackedWidget(QStackedWidget, PisakScannableItem):
    items_switched_signal = Signal(QObject, QObject)
    """
    Przechowuje różne obiekty i zarządza ich wyświetlaniem:
    - np. może wyświetlać różne keyboardy lub może wyświetlać różne moduły
    """

    def __init__(self, parent):
        super().__init__(parent)

    def add_item(self, item):
        self._items.append(item)
        if isinstance(item, PisakScannableItem):
            self._scannable_items.append(item)

    # def init_ui(self):
    #     return NotImplemented
    #
    # def set_layout(self):
    #     return NotImplemented


    # TODO dodać funkcję, która będzie zarządzała wyświetlaniem obiektów
    #  należących do PisakStackedWidget -> jak zmieni wyświetlany obiekt,
    #  to musi wysyłać sygnał do scanning managera, że obiekt został zmieniony
    #  wtedy scanning manager będzie kończył jedno skanowanie i rozpoczynał drugie
    def switch_shown_item(self, new_item):
        old_item = self.currentWidget()
        self.setCurrentWidget(new_item)
        self.items_switched_signal.emit(old_item, new_item)

class PisakButton(QPushButton, PisakScannableItem):

    # TODO chyba trzeba zmienić podejście do przycisków
    #  każdy przycisk powinien mieć pole ze swoim labelem - czyli tym,
    #  co rzeczywiście wyświetla się użytkownikowi na przycisku
    #  typu litera A, znaczek spacji, znaczek strzałki etc.
    #  dodatkowo przycisk powinien mieć pole `actions` (przykładowo)
    #  które przechowywałoby akcje, dziejące się po wciśnięciu danego przycisku
    #  np. przycisk z literą A powinien mieć akcję, żeby dodać do
    #  wyświetlonego tekstu literę A; ale z kolei przycisk z ikonką spacji,
    #  nie dodaje ikonki spacji, tylko dodaje spację (" ") do wyświetlonego
    #  tekstu -> może zatem powinno być jeszcze dodatkowe pole typu `send_text`
    #  które przechowywałoby informację, co należy przesłać, do wyświetlonego
    #  tekstu (takie pole mogłoby być stringiem lub Nonem - dla przycisków
    #  takich jak backspace lub strzałka)

    send_text_signal = Signal(str)
    send_icon_signal = Signal(QIcon)
    send_backspace_signal = Signal()
    send_arrow_signal = Signal()

    def __init__(self, parent, text="", icon=None, emit_actions=None, scanning_strategy=BackToParentStrategy()):
        super().__init__(parent=parent, text=text)
        if icon:
            self.setIcon(icon)
        self._scanning_strategy = scanning_strategy
        self._text = text
        self._emit_actions = emit_actions or []
        self.init_ui()
        self.clicked.connect(self._emit_signals)

    def _emit_signals(self):
        for signal_name, value in self._emit_actions:
            signal = getattr(self, signal_name)
            if value is not None:
                signal.emit(value)
            else:
                signal.emit()

    def init_ui(self):
        self.setFont(QFont("Arial", 16))
        self.setStyleSheet("""
                            background-color: #ede4da;
                            color: black;
                            border-style: solid;
                            border-width: 2px;
                            border-color: black;
                            border-radius: 5px;
                            min-height: 50px;
                            font-weight: bold;
                            """)

    @property
    def text(self):
        return self._text

    # test slot
    @Slot()
    def button_clicked(self) -> None:
        print(f"Button {str(self)} was clicked!")
        self.send_text_signal.emit(self._text)

    def focusInEvent(self, event: QFocusEvent):
        if event.gotFocus():
            self.highlight_all()
        else:
            super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        if event.lostFocus():
            self.reset_highlight_all()
        else:
            super().focusOutEvent(event)

    def highlight_self(self):
        self.setStyleSheet("""
                            background-color: #5ea9eb;
                            color: black;
                            border-style: solid;
                            border-width: 2px;
                            border-color: #9dccf5;
                            border-radius: 5px;
                            min-height: 50px;
                            font-weight: bold;
                            """)

    def reset_highlight_self(self):
        self.init_ui()

    def highlight_all(self):
        self.highlight_self()

    def reset_highlight_all(self):
        self.reset_highlight_self()

class PisakButtonBuilder:
    def __init__(self):
        self._text = ""
        self._icon = None
        self._emit_actions = []
        self._scanning_strategy = BackToParentStrategy()

    def set_text(self, text):
        self._text = text
        return self

    def set_icon(self, icon):
        self._icon = icon
        return self

    def set_scanning_strategy(self, strategy):
        self._scanning_strategy = strategy
        return self

    def emit_text_signal(self, value):
        self._emit_actions.append(('send_text_signal', value))
        return self

    def emit_icon_signal(self, icon):
        self._emit_actions.append(('send_icon_signal', icon))
        return self

    def emit_backspace_signal(self):
        self._emit_actions.append(('send_backspace_signal', None))
        return self

    def emit_arrow_signal(self):
        self._emit_actions.append(('send_arrow_signal', None))
        return self

    def build(self, parent):
        return PisakButton(
            parent=parent,
            text=self._text,
            icon=self._icon,
            emit_actions=self._emit_actions,
            scanning_strategy=self._scanning_strategy
        )


class PisakDisplay(QLabel):

    # TODO luźne pytanie: jak zaimplementować zarządzanie tekstem???
    #  idąc tropem scanning managera, najwygodniej byłoby gdyby za zarządzanie
    #  tekstem odpowiedzialny był jeden obiekt. To jest rozwiązanie,
    #  w stronę którego osobiście się skłaniam -> imo WSZYSTKIE modyfikacje
    #  wyświetlanego tekstu powinny być wykonywane tylko i wyłącznie przez
    #  PisakDisplay - każde dodanie litery, usunięcie znaku etc, powinno
    #  odbywać się w obrębie displaya, przyciski z klawiatury powinny tylko
    #  zapewniać odpowiednie informacje, a już sam Display powinien decydować,
    #  co z tymi informacjami zrobi
    #  pytanie natomiast, czy to jest dobre podejście oraz, jak zapewnić
    #  sensowną komunikację między przyciskami a Displayem (sygnałami ???)
    #
    # Bo jest jeszcze druga opcja, że to całe zarządzanie tekstem będzie z
    # poziomu klawiatury i że display będzie "przynależał" do klawiatury.
    # Tylko że imo to rozwiązanie jest o tyle niewygodne, że po pierwsze
    # wtedy w keyboardzie będzie się działo bardzo dużo, a po drugie chcemy
    # mieć jeden display per moduł, ale w jednym module mogą być różne klawiatury
    # (pewnie maksymalnie dwie: z małymi literami i z dużymi literami, ale to
    # zawsze trzeba by jakoś bawić się w pilnowanie, żeby zarządzały one tym
    # samym displayem)
    #
    # może napisać dekorator do inita przycisków, który dekorował by taki init
    # sygnałem, który wysyłany byłby przy wciśnięciu danego przycisku?
    # czyli np byłoby coś takiego, że przycisk z literą A udekorowany byłby
    # sygnałem send_text (dzięki dekoratorowi w inicie pojawiała by się
    # instrukcje, że kliknięcie przycisku ma być połączone z wysłaniem sygnału
    # send_text) - i wtedy takie sygnały do udekorowania danego przycisku można
    # by przekazywać w jakimś pliku z konfigami przycisków
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    #
    # obserwuje PisakStackedWidget, w którym przechowywane są klawiatury?
    # wtedy można by ręcznie połączyć sygnały przycisków ze slotami Displaya,
    # na zasadzie ten sygnał połącz z tym slotem itp

    """
    Wyświetlacz do tekstu. Zarządza wyświetlaniem tekstu i modyfikowaniem go.
    Ma swój kursor, który wskazuje, w którym miejscu modyfikujemy tekst.
    """
    def __init__(self, parent):
        super().__init__(parent=parent)

        self._cursor_index: int = 0
        self._cursor_visible: bool = True
        self._cursor_timer = QTimer()
        self._cursor_timer.timeout.connect(self.toggle_cursor)
        self._cursor_timer.start(500)
        self._text = ""

        self.init_ui()

    @property
    def cursor_index(self):
        return self._cursor_index

    @property
    def text(self):
        return self._text

    def init_ui(self):
        self.setFont(QFont("Arial", 16))
        self.setAlignment(Qt.AlignVCenter)
        self.setLineWidth(10)
        self.setStyleSheet("""
                            background-color: #f0f0f0;
                            color: black;
                            border-style: solid;
                            border-width: 2px;
                            border-color: black;
                            border-radius: 5px;
                            padding: 5px;
                            margin-bottom: 10px;
                            """)

    def connect_signals_to_slots(self, connection_config):
        """
        funkcja, która łączy sygnały obserwowanych obiektów (np. przycisków
        znajdujących się w klawiaturach) z konkretnymi funkcjami display'a;
        czyli np. łączymy sygnał
        :param connection_config:
        :return:
        """

    def toggle_cursor(self):
        """Toggle cursor visibility for blinking effect"""
        self._cursor_visible = not self._cursor_visible
        self.update()

    def move_cursor_left(self):
        # todo na razie to jest zrobione trochę na pałe,
        #  ale docelowo zrobić tak, że jeśli np mamy wielolinijkowy tekst,
        #  to jak dojdziemy do początku linii, to przesunięcie w lewo powinno
        #  nas przenieść na koniec poprzedniej linii
        if self._cursor_index > 0:
            # ten warunek jest git, ale trzeba go połączyć z tym, co wyżej
            self._cursor_index -= 1

    def move_cursor_right(self):
        if self._cursor_index < len(self._text):
            # ten warunek jest o tyle do zmiany, że nie uwzględnia tego,
            # że tekst może być wielolinijkowy i gdy dojdziemy do końca linii,
            # to przesuwając kursor w prawo, chcemy przeskoczyć na początek
            # kolejnej linii

            # może powinno być pole przetrzymujące długość aktualnie
            # modyfikowanej linii typu self.current_line_length ???
            self._cursor_index += 1

    def update_text(self, text):
        """Insert arbitrary text at the cursor position."""
        current_text = self._text
        left_text = current_text[:self._cursor_index]
        right_text = current_text[self._cursor_index:]
        self._text = left_text + text + right_text
        self._cursor_index += len(text)
        self.update()

    def insert_newline(self):
        """Insert a newline at the cursor position."""
        self.update_text("\n")

    def add_space(self):
        self.update_text(" ")

    def paintEvent(self, event):
        """Custom paint event to draw multi-line text and cursor."""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setFont(self.font())

        text_rect = self.rect().adjusted(*(10, 0), *(-10, 0))  # Padding
        font_metrics = QFontMetrics(self.font())
        line_spacing = font_metrics.lineSpacing()

        # Split text into lines
        lines = self._text.split("\n")

        # Find cursor line and column
        cursor_line = 0
        cursor_col = 0
        chars_seen = 0
        for i, line in enumerate(lines):
            if self._cursor_index <= chars_seen + len(line):
                cursor_line = i
                cursor_col = self._cursor_index - chars_seen
                break
            chars_seen += len(line) + 1  # +1 for the '\n'
        else:
            cursor_line = len(lines) - 1
            cursor_col = len(lines[-1])

        # Calculate vertical centering offset for all lines
        total_text_height = line_spacing * len(lines)
        available_height = text_rect.height()
        y_offset = text_rect.top() + (available_height - total_text_height) // 2

        # Draw each line and find cursor position
        cursor_x = 0
        cursor_y = 0
        for i, line in enumerate(lines):
            y = y_offset + i * line_spacing + font_metrics.ascent()
            painter.drawText(text_rect.left(), y, line)
            if i == cursor_line:
                cursor_x = text_rect.left() + font_metrics.horizontalAdvance(line[:cursor_col])
                cursor_y = y

        # Draw cursor if visible
        if self._cursor_visible:
            cursor_pen = QPen(Qt.black)
            cursor_width = max(1, self.font().pointSize() // 8)
            cursor_pen.setWidth(cursor_width)
            painter.setPen(cursor_pen)
            cursor_height = font_metrics.height()
            cursor_y_top = cursor_y - font_metrics.ascent()
            cursor_y_bottom = cursor_y_top + cursor_height
            painter.drawLine(cursor_x, cursor_y_top, cursor_x, cursor_y_bottom)


