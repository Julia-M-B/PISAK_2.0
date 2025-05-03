import os
import sys
from functools import partial

from PySide6.QtWidgets import (QApplication, QStackedWidget, QVBoxLayout,
                               QWidget)

from pisak.apps.base_app import PisakAppsWidget, PisakBaseApp
from pisak.apps.main_menu.app import PisakMainApp
from pisak.apps.speller.app import PisakSpellerApp
from pisak.apps.symboler.app import PisakSymbolerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = QWidget()
    print(os.getpid())

    windows = PisakAppsWidget(parent=main_widget)
    windows.closeEvent = lambda event: app.quit()

    MainWindow = PisakMainApp(parent=windows)
    SpellerWindow = PisakSpellerApp(parent=windows)
    SymbolerWindow = PisakSymbolerApp(parent=windows)

    windows.addWidget(MainWindow)
    windows.addWidget(SpellerWindow)
    windows.addWidget(SymbolerWindow)

    switch_to_speller = partial(windows.switch_to_window, SpellerWindow)
    switch_to_symboler = partial(windows.switch_to_window, SymbolerWindow)

    MainWindow.speller_btn.clicked.connect(switch_to_speller)
    MainWindow.symboler_btn.clicked.connect(switch_to_symboler)

    windows.switch_to_window(MainWindow)

    sys.exit(app.exec())
