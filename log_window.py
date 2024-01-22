from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QTextEdit, QWidget, QApplication
from PyQt6.QtGui import QIcon
from database import Database

class LogWindow(QMainWindow):
    """Класс интерфейса окна журнала событий"""
    def __init__(self, log_entries=None, parent=None):
        super(LogWindow, self).__init__(parent)
        self.setWindowTitle('Журнал событий')
        self.setGeometry(100, 100, 800, 600)
        icon = QIcon('log1.png')
        self.setWindowIcon(icon)
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
        """Метод, вызываемый при закрытии окна. Сохраняет данные в базе данных"""
        self.save_log_to_database()
        event.accept()

    def save_log_to_database(self):
        """Метод для сохранения данных журнала в базу данных"""
        self.database.connection.commit()

    def load_log_from_database(self):
        """Метод для загрузки данных журнала событий из базы данных и их отображение"""
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