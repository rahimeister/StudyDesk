from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox


class TopicsPage(QWidget):
    def __init__(self, manager, on_data_changed):
        super().__init__(); self.manager=manager; self.on_data_changed=on_data_changed
        root=QVBoxLayout(self)
        title=QLabel("Ders / Konu Takibi"); title.setObjectName("pageTitle"); root.addWidget(title)
        form=QHBoxLayout()
        self.subject=QLineEdit(); self.subject.setPlaceholderText("Ders adı")
        self.topic=QLineEdit(); self.topic.setPlaceholderText("Konu başlığı")
        self.priority=QComboBox(); self.priority.addItems(["Yüksek","Orta","Düşük"])
        self.target=QSpinBox(); self.target.setRange(5,10000); self.target.setValue(180); self.target.setSuffix(" dk")
        add=QPushButton("Konu Ekle"); add.clicked.connect(self.add_topic)
        for w in [self.subject,self.topic,self.priority,self.target,add]: form.addWidget(w)
        root.addLayout(form)
        self.table=QTableWidget(0,7); self.table.setHorizontalHeaderLabels(["ID","Ders","Konu","Durum","Öncelik","Hedef","Çalışılan"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows); self.table.setEditTriggers(QTableWidget.NoEditTriggers); self.table.setColumnHidden(0,True)
        self.table.horizontalHeader().setStretchLastSection(True); root.addWidget(self.table)
        actions=QHBoxLayout()
        complete=QPushButton("Tamamlandı Yap"); complete.clicked.connect(lambda:self.set_status("Tamamlandı"))
        ongoing=QPushButton("Devam Ediyor Yap"); ongoing.clicked.connect(lambda:self.set_status("Devam Ediyor"))
        delete=QPushButton("Seçileni Sil"); delete.setObjectName("dangerButton"); delete.clicked.connect(self.delete_selected)
        actions.addWidget(complete); actions.addWidget(ongoing); actions.addWidget(delete); actions.addStretch(); root.addLayout(actions)
        self.refresh()

    def selected_id(self):
        row=self.table.currentRow()
        return int(self.table.item(row,0).text()) if row>=0 else None

    def add_topic(self):
        try:
            self.manager.add_topic(self.subject.text(),self.topic.text(),self.priority.currentText(),self.target.value())
            self.topic.clear(); self.refresh(); self.on_data_changed()
        except Exception as e: QMessageBox.warning(self,"Hata",str(e))

    def set_status(self,status):
        tid=self.selected_id()
        if not tid: return
        self.manager.update_topic_status(tid,status); self.refresh(); self.on_data_changed()

    def delete_selected(self):
        tid=self.selected_id()
        if not tid: return
        if QMessageBox.question(self,"Sil","Seçili konu silinsin mi?")==QMessageBox.Yes:
            self.manager.delete_topic(tid); self.refresh(); self.on_data_changed()

    def refresh(self):
        self.table.setRowCount(0)
        for t in self.manager.get_topics():
            r=self.table.rowCount(); self.table.insertRow(r)
            vals=[t['id'],t['subject_name'],t['title'],t['status'],t['priority'],f"{t['target_minutes']} dk",f"{t['studied_minutes']} dk"]
            for c,v in enumerate(vals): self.table.setItem(r,c,QTableWidgetItem(str(v)))
