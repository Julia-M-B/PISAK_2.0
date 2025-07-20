import sys

from PySide6.QtWidgets import QApplication

from pisak.modules.speller.module import PisakSpellerModule
from pisak.scanning.manager import manager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    SpellerWindow = PisakSpellerModule()
    SpellerWindow.show()
    # print(SpellerWindow.centralWidget().items)
    manager.manager.manage_scanning_module(SpellerWindow)
    # manager.manager.change_scanned_item(SpellerWindow.centralWidget())
    sys.exit(app.exec())
