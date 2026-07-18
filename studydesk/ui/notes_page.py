from pathlib import Path
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QTextEdit,QPushButton,QTableWidget,QTableWidgetItem,QMessageBox,QFileDialog
from file_exporter import export_notes


class NotesPage(QWidget):
    def __init__(self, manager):
        super().__init__(); self.manager=manager
        root=QVBoxLayout(self)
        title=QLabel("Notlar"); title.setObjectName("pageTitle"); root.addWidget(title)
        self.topic=QComboBox(); self.title_input=QLineEdit(); self.title_input.setPlaceholderText("Not başlığı")
        self.content=QTextEdit(); self.content.setPlaceholderText("Not içeriği...")
        root.addWidget(self.topic); root.addWidget(self.title_input); root.addWidget(self.content)
        row=QHBoxLayout(); save=QPushButton("Notu Kaydet"); save.clicked.connect(self.save_note); export=QPushButton("TXT Dışa Aktar"); export.clicked.connect(self.export)
        row.addWidget(save); row.addWidget(export); row.addStretch(); root.addLayout(row)
        self.table=QTableWidget(0,5); self.table.setHorizontalHeaderLabels(["ID","Başlık","Ders/Konu","İçerik","Tarih"]); self.table.setColumnHidden(0,True); self.table.setSelectionBehavior(QTableWidget.SelectRows); self.table.setEditTriggers(QTableWidget.NoEditTriggers); self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)
        delete=QPushButton("Seçili Notu Sil"); delete.setObjectName("dangerButton"); delete.clicked.connect(self.delete_note); root.addWidget(delete)
        self.refresh_topics(); self.refresh()

    def refresh_topics(self):
        self.topic.clear(); self.topic.addItem("Konu seçilmedi",None)
        for t in self.manager.get_topics(): self.topic.addItem(f"{t['subject_name']} - {t['title']}",t['id'])
    def save_note(self):
        try:
            self.manager.add_note(self.topic.currentData(),self.title_input.text(),self.content.toPlainText())
            self.title_input.clear(); self.content.clear(); self.refresh()
        except Exception as e: QMessageBox.warning(self,"Hata",str(e))
    def refresh(self):
        self.table.setRowCount(0)
        for n in self.manager.get_notes():
            r=self.table.rowCount(); self.table.insertRow(r)
            vals=[n['id'],n['title'],f"{n['subject_name'] or '-'} / {n['topic_title'] or '-'}",n['content'],n['created_at']]
            for c,v in enumerate(vals): self.table.setItem(r,c,QTableWidgetItem(str(v)))
    def delete_note(self):
        row=self.table.currentRow()
        if row<0:return
        self.manager.delete_note(int(self.table.item(row,0).text())); self.refresh()
    def export(self):
        folder=QFileDialog.getExistingDirectory(self,"Dışa Aktarma Klasörü",str(Path.cwd()/"exports"))
        if folder:
            path=export_notes(self.manager.get_notes(),folder); QMessageBox.information(self,"Tamamlandı",f"Notlar dışa aktarıldı:\n{path}")
