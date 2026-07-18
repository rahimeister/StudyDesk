from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class PomodoroEngine(QObject):
    tick = pyqtSignal(int)
    finished = pyqtSignal()
    state_changed = pyqtSignal(str)

    def __init__(self, minutes=25):
        super().__init__()
        self.default_seconds = minutes * 60
        self.remaining_seconds = self.default_seconds
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._on_tick)

    def start(self):
        if self.remaining_seconds <= 0:
            self.reset()
        self.timer.start()
        self.state_changed.emit("Çalışıyor")

    def pause(self):
        self.timer.stop()
        self.state_changed.emit("Duraklatıldı")

    def reset(self, minutes=None):
        self.timer.stop()
        if minutes is not None:
            self.default_seconds = minutes * 60
        self.remaining_seconds = self.default_seconds
        self.tick.emit(self.remaining_seconds)
        self.state_changed.emit("Hazır")

    def _on_tick(self):
        self.remaining_seconds -= 1
        self.tick.emit(self.remaining_seconds)
        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.state_changed.emit("Tamamlandı")
            self.finished.emit()
