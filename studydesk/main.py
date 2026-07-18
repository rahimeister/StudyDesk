import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from database import init_db
from study_manager import StudyManager
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    try:
        init_db()
        window = MainWindow(StudyManager())
        window.show()
        sys.exit(app.exec_())
    except Exception as exc:
        QMessageBox.critical(None, "StudyDesk Hatası", str(exc))
        raise


if __name__ == "__main__":
    main()
