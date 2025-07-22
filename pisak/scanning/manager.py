from PySide6.QtCore import QTimer, Slot, QObject, Signal
from PySide6.QtWidgets import QMainWindow, QWidget

from pisak.scanning.scannable import PisakScannableItem
from pisak.utils import Singleton
from pisak.config import SCAN_HIGHLIGHT_TIME, SCAN_LOOP_NUMBER

import types
from functools import wraps

from pisak.widgets.elements import PisakButton

QtMeta = type(QMainWindow)

class ScannableManagerMeta(QtMeta):
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)

        object_dict_items = cls.__dict__.items()
        object_functions = ((name, function) for (name, function)  in object_dict_items if isinstance(function, types.FunctionType))
        for function_name, function in object_functions:
            match function_name:
                case "__init__":
                    setattr(cls, function_name, mcls._wrap__init__(function))

        # TODO sprawdzić czy wszystkie metody są zaimplementowane
        return cls

    @staticmethod
    def _wrap__init__(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            manager.new_manager()
            return result
        print("new init")
        return wrapper

    @staticmethod
    def _wrap__exit__(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            manager.delete_manager()
            return result

        return wrapper

class _ScanningManager(QWidget):
    last_id = 0
    reset_scanning = Signal(QObject)

    def __init__(self):
        super().__init__()
        self.name = f"ManagerWorker {_ScanningManager.last_id}"
        _ScanningManager.last_id += 1
        print(f"Initializing ManagerWorker {self}")

        self.timer = QTimer()
        self.timer.timeout.connect(self.set_focus_on_item)
        # self.managed_module = None
        self.scanned_item = None

        self.reset_scanning.connect(self.change_scanned_item)


    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def run(self):
        print(f"Running {self.name}")

    def stop(self):
        print(f"Stoping {self}")

    def manage_scanning_module(self, module):
        module.start_scanning.connect(self.change_scanned_item)
        module.key_pressed.connect(self.key_press_handler)

    # TODO teraz, jeśli w wierszu/kolumnie jest tylko jeden element,
    #  to jest on skanowany tak jakby "3 razy pod rząd", bez żadnej przerwy
    #  należałoby dodać jakiś warunek, że jeśli dany container ma tylko jeden element
    #  to zamiast wykonywać SCAN_LOOP_NUMBER pętli skanowania,
    #  przeskanować go tylko raz, bo teraz wygląda to tak, jakby coś się zacięło



    def scan(self):
        print(f"Scanning {self.scanned_item} with {self}")
        self.timer.start(SCAN_HIGHLIGHT_TIME * 1000)
        iter(self.scanned_item)
        self.set_focus_on_item()

    def set_focus_on_item(self):
        if self.scanned_item.loops_counter == SCAN_LOOP_NUMBER * len(self.scanned_item.items):
            self.reset_scan()
            return
        print("in scan_item function")
        focused_item = next(self.scanned_item)
        print(f"Scanned item: {focused_item}")
        focused_item.setFocus()

    def stop_scanning(self):
        self.timer.stop()
        print(f"Stoping scanning for {self}")
        # TODO zmienić loop_counter na prywatny i dodać setter
        self.scanned_item.loops_counter = 0

    def reset_scan(self):
        self.stop_scanning()
        new_item = self.scanned_item.scanning_strategy.reset_scan(self.scanned_item)
        if not isinstance(new_item, PisakScannableItem):
            new_item.setFocus()
            return
        self.reset_scanning.emit(new_item)

    @Slot()
    def key_press_handler(self):
        focused_widget = self.scanned_item.focusWidget()
        if focused_widget in self.scanned_item.items:
            if isinstance(focused_widget, PisakButton):
                # gdy skanowany jest przycisk, to po kliknięciu na niego,
                # chcemy skanować od nowa całą klawiaturę,
                # a nie tylko jeden z jej rzędów
                self.stop_scanning()
                focused_widget.click()
                new_item = self.scanned_item.scanning_strategy.reset_scan(
                    self.scanned_item)
                self.change_scanned_item(new_item)
            else:
                self.change_scanned_item(focused_widget)


    @Slot(QObject)
    def change_scanned_item(self, scannable_item):
        if self.timer.isActive():
            self.stop_scanning()
        self.scanned_item = scannable_item
        # self.scanned_item.widget_chosen.connect(self.change_scanned_item)
        self.scan()



class NoManagerFoundError(Exception):
    pass



class Manager(metaclass=Singleton):
    _managers = []

    def __init__(self):
        print(f"Initializing Manager {self}")
        # Don't create a worker automatically during Manager initialization

    @property
    def manager(self):
        try:
            return self._managers[-1]
        except IndexError:
            raise NoManagerFoundError("No manager found")

    def new_manager(self):
        print("new_manager")
        try:
            for m in self._managers:
                m.stop()
            new_manager = _ScanningManager()
            self._managers.append(new_manager)
            return new_manager
        except Exception as e:
            print(f"Error: {e}")

    def delete_manager(self):
        if self._managers:
            manager_to_delete = self._managers[-1]
            print(f"Deleting manager {manager_to_delete}")
            self._managers.pop()
        else:
            print("No managers to delete")

        # run previous manager
        if self._managers:
            self.manager.run()

    def scan(self, scannable_item):
        self.manager.change_scanned_item(scannable_item)


    def __str__(self):
        try:
            return f"Manager with {len(self._managers)} managers {self._managers}, using {self.manager}"
        except NoManagerFoundError:
            return f"Manager with {len(self._managers)} managers {self._managers}"


manager = Manager()
