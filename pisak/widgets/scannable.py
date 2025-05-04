import copy
from time import sleep

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QWidget

from pisak.config import SCAN_HIGHLIGHT_TIME, SCAN_LOOP_NUMBER
from pisak.utils import get_id


class LoopItemsWorker(QObject):
    finished = Signal()
    next_item = Signal()
    running = False
    loops_counter = 0

    def __str__(self):
        return f"Worker {id(self)}"

    def run(self):
        print(f"Running worker {id(self)}")
        self.running = True
        while self.running:
            self.next_item.emit()
            sleep(SCAN_HIGHLIGHT_TIME)
            print(f"Worker {id(self)} is sleeping")
        self.finished.emit()
        print(f"Finishing worker {id(self)}")

    def stop(self):
        self.running = False
        print(f"Stopping worker {id(self)}")


class LoopItemsRunnable(QRunnable):
    def __init__(self, worker: LoopItemsWorker):
        super().__init__()
        self.worker = worker

    def run(self):
        self.worker.run()


class PisakScannableItem:
    end_scan_signal = NotImplemented

    def __init__(self, *args, **kwargs):
        self._id = get_id()
        self._items = []
        self._scanning_worker = None
        self._scanning_runner = None
        self._scanning_strategy = None

    def __str__(self):
        return f"{self.__class__.__name__} id={self._id}"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        self._iter_items = iter(self._items)
        return self

    def __next__(self):
        try:
            item = next(self._iter_items)
            print("Next item", item)
            return item
        except StopIteration:
            # raise
            print("Recurrent next call")
            self._scanning_worker.loops_counter += 1
            return next(iter(self))

    @property
    def items(self):
        return copy.copy(self._items)

    def add_item(self, item):
        return NotImplemented

    def init_ui(self):
        return NotImplemented

    def set_layout(self):
        return NotImplemented

    def scan(self):
        return NotImplemented

    def scan_item(self):
        return NotImplemented

    def stop_scanning(self):
        return NotImplemented

    def reset_scan(self):
        return NotImplemented

    def highlight_all(self):
        return NotImplemented

    def reset_highlight_all(self):
        return NotImplemented


class PisakScannableWidget(QWidget, PisakScannableItem):
    end_scan_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.end_scan_signal.connect(self.loop_number_exceeded)
        self.end_scan_signal.connect(self.reset_scan)

    def add_item(self, item):
        if not isinstance(item, PisakScannableItem):
            raise ValueError("Item should be PisakScannableItem.")
        self._items.append(item)

    def scan(self):
        iter(self)
        pool = QThreadPool.globalInstance()
        self._scanning_worker = LoopItemsWorker()
        self._scanning_runner = LoopItemsRunnable(self._scanning_worker)
        pool.start(self._scanning_runner)
        self._scanning_worker.next_item.connect(self.scan_item)

    def scan_item(self):
        if self._scanning_worker.loops_counter == SCAN_LOOP_NUMBER:
            print("Emitting end loop")
            self.end_scan_signal.emit()
            return
        # try:
        print("in scan_item function")
        item = next(self)
        print(f"Scanned item: {item}")
        item.setFocus()

    def stop_scanning(self):
        self._scanning_worker.stop()
        print("Stoping scanning worker")

    def reset_scan(self):
        self.stop_scanning()
        self._scanning_strategy.reset_scan(self)

    def highlight_all(self):
        for item in self.items:
            item.highlight_all()

    def reset_highlight_all(self):
        for item in self.items:
            item.reset_highlight_all()

    # for test
    def loop_number_exceeded(self):
        print(
            f"Worker {id(self._scanning_worker)} loop counter equals to {self._scanning_worker.loops_counter}"
        )
