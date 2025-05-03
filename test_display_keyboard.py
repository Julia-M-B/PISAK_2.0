import sys

from PySide6.QtWidgets import QApplication

from pisak.apps.speller.app import PisakSpellerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    SpellerWindow = PisakSpellerApp()
    SpellerWindow.show()
    sys.exit(app.exec())
