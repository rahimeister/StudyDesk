from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QTableWidget, QTableWidgetItem, QPushButton, QSpinBox, QFrame
from ui.common import stat_card


class DashboardPage(QWidget):
    def __init__(self, manager, on_navigate):
        super().__init__()
        self.manager = manager
        root = QVBoxLayout(self)
        header = QLabel("Dashboard")
        header.setObjectName("pageTitle")
        root.addWidget(header)

        cards = QHBoxLayout()
        self.today_card = stat_card("Bugünkü Çalışma", "0 dk")
        self.pomodoro_card = stat_card("Tamamlanan Pomodoro", "0")
        self.goal_card = stat_card("Günlük Hedef", "0 dk")
        self.success_card = stat_card("Başarı", "%0")
        for c in [self.today_card, self.pomodoro_card, self.goal_card, self.success_card]: cards.addWidget(c)
        root.addLayout(cards)

        goal_box = QFrame(); goal_box.setObjectName("card")
        goal_layout = QVBoxLayout(goal_box)
        goal_row = QHBoxLayout()
        goal_row.addWidget(QLabel("Günlük hedef (dakika):"))
        self.goal_spin = QSpinBox(); self.goal_spin.setRange(25, 1440); self.goal_spin.setSingleStep(25)
        save_goal = QPushButton("Hedefi Kaydet"); save_goal.clicked.connect(self.save_goal)
        goal_row.addWidget(self.goal_spin); goal_row.addWidget(save_goal); goal_row.addStretch()
        self.progress = QProgressBar(); self.progress.setRange(0,100)
        goal_layout.addLayout(goal_row); goal_layout.addWidget(self.progress)
        root.addWidget(goal_box)

        quick = QHBoxLayout()
        p = QPushButton("Pomodoro Başlat"); p.clicked.connect(lambda: on_navigate(1))
        n = QPushButton("Not Ekle"); n.clicked.connect(lambda: on_navigate(3))
        quick.addWidget(p); quick.addWidget(n); quick.addStretch()
        root.addLayout(quick)

        root.addWidget(QLabel("Son Çalışmalar"))
        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Ders", "Konu", "Süre", "Tarih"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table)
        self.refresh()

    def save_goal(self):
        self.manager.set_daily_goal(self.goal_spin.value())
        self.refresh()

    def refresh(self):
        s = self.manager.dashboard_stats()
        self.today_card.value_label.setText(f"{s['today_minutes']} dk")
        self.pomodoro_card.value_label.setText(str(s['pomodoros']))
        self.goal_card.value_label.setText(f"{s['goal']} dk")
        percent = min(100, int(s['today_minutes'] / s['goal'] * 100)) if s['goal'] else 0
        self.success_card.value_label.setText(f"%{percent}")
        self.progress.setValue(percent)
        self.goal_spin.setValue(s['goal'])
        self.table.setRowCount(0)
        for row in s['recent']:
            r = self.table.rowCount(); self.table.insertRow(r)
            vals = [row['subject_name'], row['topic_title'], f"{row['duration_minutes']} dk", row['created_at']]
            for c,v in enumerate(vals): self.table.setItem(r,c,QTableWidgetItem(str(v)))
