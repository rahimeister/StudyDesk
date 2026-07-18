from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QProgressBar,QFrame
from ui.common import stat_card


class StatsPage(QWidget):
    def __init__(self, manager):
        super().__init__(); self.manager=manager
        root=QVBoxLayout(self); title=QLabel("İstatistikler"); title.setObjectName("pageTitle"); root.addWidget(title)
        cards=QHBoxLayout(); self.total=stat_card("Toplam Çalışma","0 dk"); self.top=stat_card("En Çok Çalışılan Ders","-"); self.completed=stat_card("Tamamlanan Konu","0"); self.week=stat_card("Bu Hafta Tamamlanan","0")
        for c in [self.total,self.top,self.completed,self.week]: cards.addWidget(c)
        root.addLayout(cards)
        box=QFrame(); box.setObjectName("card"); layout=QVBoxLayout(box); layout.addWidget(QLabel("Bugünkü hedef ilerlemesi")); self.progress=QProgressBar(); layout.addWidget(self.progress); root.addWidget(box); root.addStretch(); self.refresh()
    def refresh(self):
        s=self.manager.dashboard_stats(); self.total.value_label.setText(f"{s['total_minutes']} dk"); self.top.value_label.setText(s['top_subject']); self.completed.value_label.setText(str(s['completed_topics'])); self.week.value_label.setText(str(s['completed_week'])); self.progress.setValue(min(100,int(s['today_minutes']/s['goal']*100)) if s['goal'] else 0)
