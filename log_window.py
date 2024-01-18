from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from database import Database

class LogWindow(QMainWindow):
    def __init__(self, log_entries=None, parent=None):
        super(LogWindow, self).__init__(parent)

        self.setWindowTitle('Log Window')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.layout.addWidget(self.log_text_edit)

        self.database = Database("products.db")

        if not log_entries:
            self.load_log_from_database()

        self.load_log_from_database()

    def closeEvent(self, event):

        self.save_log_to_database()
        event.accept()

    def save_log_to_database(self):
        self.database.connection.commit()

    def load_log_from_database(self):
        log_entries = self.database.load_log_from_database()
        
        for entry in log_entries:
            self.log_text_edit.append(entry)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    log_window = LogWindow()
    log_window.show()
    sys.exit(app.exec())