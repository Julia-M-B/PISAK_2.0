import sys

from PySide6.QtWidgets import QApplication

from pisak.modules.speller.module import PisakSpellerModule

if __name__ == "__main__":
    app = QApplication(sys.argv)

    SpellerWindow = PisakSpellerModule()
    SpellerWindow.show()
    sys.exit(app.exec())
