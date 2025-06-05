from PySide6.QtCore import Qt
from PySide6.QtGui import QFocusEvent, QKeyEvent
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout

from pisak.widgets.elements import PisakButton
from pisak.widgets.scannable import PisakScannableWidget
from pisak.widgets.strategies import BackToParentStrategy, Strategy


class PisakContainerWidget(PisakScannableWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent)
        self._scanning_strategy = strategy
        self._layout = QGridLayout()

    @property
    def layout(self):
        return self._layout

    def set_layout(self) -> None:
        for item in self._items:
            self._layout.addWidget(item)
        self.setLayout(self._layout)

    def init_ui(self):
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event: QKeyEvent):
        """Intercept key press events."""
        if event.key() == Qt.Key_1:
            focused_widget = self.focusWidget()
            if focused_widget in self.items:
                self._scanning_worker.stop()
                focused_widget.scan()
                return
        super().keyPressEvent(event)

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


class PisakGridWidget(PisakContainerWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent, strategy)
        self._layout = QGridLayout()

    def reset_scan(self):
        # funkcja domyślnie podłączona do sygnału end_scan_signal
        # w inicie klasy-rodzica: PisakScannableWidget

        # nadpisanie funkcji reset_scan z klasy-rodzica: PisakScannableWidget
        # normalnie ta funkcja wywołuje funkcję reset_scan pochodzącą
        # z danej strategii skanowania

        # w tym przypadku fukncja powinna kończyć całe skanowanie i
        # usuwać focus z elementu (jeśli takowy jest)
        focused_widget = self.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()
        self.stop_scanning()


class PisakColumnWidget(PisakContainerWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent, strategy)
        self._layout = QVBoxLayout()


class PisakRowWidget(PisakContainerWidget):
    def __init__(self, parent, strategy: Strategy = BackToParentStrategy()):
        super().__init__(parent, strategy)
        self._layout = QHBoxLayout()

    # PisakRowWidget should only contain PisakButtons
    def add_item(self, item):
        if not isinstance(item, PisakButton):
            raise ValueError("Item should be PisakButton.")
        self._items.append(item)

