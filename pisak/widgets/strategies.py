from pisak.widgets.scannable import PisakScannableItem


class Strategy:
    @staticmethod
    def reset_scan(arg):
        return NotImplemented

    @staticmethod
    def count_scanning_loops(arg):
        return NotImplemented


class BackToParentStrategy(Strategy):
    @staticmethod
    def reset_scan(obj: PisakScannableItem) -> None:
        obj.parentWidget().scan()


class BackToTopStrategy(Strategy):
    @staticmethod
    def reset_scan(obj: PisakScannableItem) -> None:
        obj.parentWidget().reset_scan()


class TopStrategy(Strategy):
    @staticmethod
    def reset_scan(obj: PisakScannableItem) -> None:
        obj.scan()
