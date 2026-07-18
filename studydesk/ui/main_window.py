from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QLabel,QStackedWidget,QFrame
from ui.dashboard_page import DashboardPage
from ui.pomodoro_page import PomodoroPage
from ui.topics_page import TopicsPage
from ui.notes_page import NotesPage
from ui.stats_page import StatsPage

STYLE="""
QWidget { background:#111827; color:#e5e7eb; font-family:'Segoe UI'; font-size:14px; }
QFrame#sidebar { background:#0b1220; border-right:1px solid #243047; }
QPushButton { background:#2563eb; color:white; border:none; border-radius:8px; padding:10px 14px; font-weight:600; }
QPushButton:hover { background:#1d4ed8; }
QPushButton#navButton { text-align:left; background:transparent; padding:12px; }
QPushButton#navButton:hover { background:#1f2937; }
QPushButton#dangerButton { background:#dc2626; }
QFrame#card { background:#1f2937; border:1px solid #334155; border-radius:12px; }
QLabel#pageTitle { font-size:28px; font-weight:700; margin-bottom:8px; }
QLabel#brand { font-size:24px; font-weight:800; color:#60a5fa; padding:10px; }
QLabel#statValue { font-size:24px; font-weight:700; color:white; }
QLabel#muted { color:#9ca3af; }
QLabel#timerLabel { font-size:76px; font-weight:800; color:#60a5fa; padding:28px; }
QLineEdit,QTextEdit,QComboBox,QSpinBox,QTableWidget { background:#182235; border:1px solid #334155; border-radius:7px; padding:7px; }
QHeaderView::section { background:#243047; padding:8px; border:none; font-weight:600; }
QProgressBar { background:#182235; border:none; border-radius:7px; text-align:center; height:18px; }
QProgressBar::chunk { background:#2563eb; border-radius:7px; }
"""


class MainWindow(QMainWindow):
    def __init__(self, manager):
        super().__init__(); self.manager=manager
        self.setWindowTitle("StudyDesk"); self.resize(1250,760); self.setStyleSheet(STYLE)
        central=QWidget(); self.setCentralWidget(central); root=QHBoxLayout(central); root.setContentsMargins(0,0,0,0)
        sidebar=QFrame(); sidebar.setObjectName("sidebar"); sidebar.setFixedWidth(210); side=QVBoxLayout(sidebar)
        brand=QLabel("StudyDesk"); brand.setObjectName("brand"); side.addWidget(brand)
        self.stack=QStackedWidget()
        self.dashboard=DashboardPage(manager,self.navigate); self.pomodoro=PomodoroPage(manager,self.refresh_all); self.topics=TopicsPage(manager,self.refresh_all); self.notes=NotesPage(manager); self.stats=StatsPage(manager)
        for p in [self.dashboard,self.pomodoro,self.topics,self.notes,self.stats]: self.stack.addWidget(p)
        for i,text in enumerate(["Dashboard","Pomodoro","Konular","Notlar","İstatistikler"]):
            b=QPushButton(text); b.setObjectName("navButton"); b.clicked.connect(lambda _,x=i:self.navigate(x)); side.addWidget(b)
        side.addStretch(); side.addWidget(QLabel("Python • PyQt5 • SQLite")); root.addWidget(sidebar); root.addWidget(self.stack,1)
    def navigate(self,index):
        self.stack.setCurrentIndex(index); self.refresh_all()
    def refresh_all(self):
        self.dashboard.refresh(); self.pomodoro.refresh_topics(); self.topics.refresh(); self.notes.refresh_topics(); self.notes.refresh(); self.stats.refresh()
