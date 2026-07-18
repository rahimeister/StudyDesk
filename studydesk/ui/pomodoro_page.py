from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QPushButton,QMessageBox,QSpinBox
from PyQt5.QtCore import Qt
from pomodoro import PomodoroEngine


class PomodoroPage(QWidget):
    def __init__(self, manager, on_data_changed):
        super().__init__(); self.manager=manager; self.on_data_changed=on_data_changed
        self.engine=PomodoroEngine(25); self.elapsed=0
        root=QVBoxLayout(self)
        title=QLabel("Pomodoro"); title.setObjectName("pageTitle"); root.addWidget(title)
        self.topic_combo=QComboBox(); root.addWidget(self.topic_combo)
        duration_row=QHBoxLayout(); duration_row.addWidget(QLabel("Çalışma süresi:"))
        self.minutes=QSpinBox(); self.minutes.setRange(1,180); self.minutes.setValue(25); self.minutes.setSuffix(" dk"); self.minutes.valueChanged.connect(self.change_duration)
        duration_row.addWidget(self.minutes); duration_row.addStretch(); root.addLayout(duration_row)
        self.timer_label=QLabel("25:00"); self.timer_label.setAlignment(Qt.AlignCenter); self.timer_label.setObjectName("timerLabel"); root.addWidget(self.timer_label)
        self.status=QLabel("Hazır"); self.status.setAlignment(Qt.AlignCenter); self.status.setObjectName("muted"); root.addWidget(self.status)
        buttons=QHBoxLayout()
        for text,fn in [("Başlat",self.start),("Duraklat",self.engine.pause),("Sıfırla",self.reset),("Bitir ve Kaydet",self.finish_save)]:
            b=QPushButton(text); b.clicked.connect(fn); buttons.addWidget(b)
        root.addLayout(buttons); root.addStretch()
        self.engine.tick.connect(self.update_time); self.engine.finished.connect(self.auto_finished); self.engine.state_changed.connect(self.status.setText)
        self.refresh_topics()

    def refresh_topics(self):
        current=self.topic_combo.currentData(); self.topic_combo.clear()
        self.topic_combo.addItem("Genel çalışma",None)
        for t in self.manager.get_topics(False): self.topic_combo.addItem(f"{t['subject_name']} - {t['title']}",t['id'])
        idx=self.topic_combo.findData(current)
        if idx>=0:self.topic_combo.setCurrentIndex(idx)

    def change_duration(self,v): self.engine.reset(v); self.elapsed=0
    def start(self): self.engine.start()
    def reset(self): self.engine.reset(self.minutes.value()); self.elapsed=0
    def update_time(self,seconds):
        self.elapsed=self.minutes.value()*60-seconds
        self.timer_label.setText(f"{seconds//60:02d}:{seconds%60:02d}")
    def auto_finished(self):
        QMessageBox.information(self,"Pomodoro","Çalışma süresi tamamlandı. Süre kaydediliyor.")
        self.save_minutes(self.minutes.value()); self.reset()
    def finish_save(self):
        mins=max(1,self.elapsed//60)
        self.save_minutes(mins); self.reset()
    def save_minutes(self,mins):
        try:
            self.manager.add_session(self.topic_combo.currentData(),mins,"Pomodoro")
            self.on_data_changed(); QMessageBox.information(self,"Kaydedildi",f"{mins} dakika çalışma kaydedildi.")
        except Exception as e: QMessageBox.warning(self,"Hata",str(e))
