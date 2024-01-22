from PyQt6 import QtCore, QtGui, QtWidgets

class SearchWindow(QtWidgets.QWidget):
    """Сигналы для поиска товара и отмены поиска"""
    searchProductSignal = QtCore.pyqtSignal(str)
    cancelSearchSignal = QtCore.pyqtSignal()

    def __init__(self):
        """Инициализация окна поиска товара"""
        super().__init__()
        self.ui = Ui_SearchWindow()
        self.ui.setupUi(self)
        self.ui.searchButton.clicked.connect(self.emitSearchProductSignal)
        self.ui.cancelButton.clicked.connect(self.cancelSearch)

    def emitSearchProductSignal(self):
        """Метод для отправки сигнала с запросом на поиск товара"""
        search_term = self.ui.searchLineEdit.text()
        self.searchProductSignal.emit(search_term)

    def cancelSearch(self):
        """Метод для отправки сигнала об отмене поиска"""
        self.cancelSearchSignal.emit()

class Ui_SearchWindow(object):
    def setupUi(self, SearchWin):
        """Метод для настройки интерфейса окна поиска товара"""
        SearchWin.setObjectName("SearchWindow")
        SearchWin.resize(400, 100)
        SearchWin.setWindowTitle("Поиск")
        self.gridLayout = QtWidgets.QGridLayout(SearchWin)
        self.gridLayout.setObjectName("gridLayout")
        self.searchLabel = QtWidgets.QLabel(SearchWin)
        self.searchLabel.setText("Введите название товара:")
        self.gridLayout.addWidget(self.searchLabel, 0, 0, 1, 1)
        self.searchLineEdit = QtWidgets.QLineEdit(SearchWin)
        self.gridLayout.addWidget(self.searchLineEdit, 0, 1, 1, 1)
        self.searchButton = QtWidgets.QPushButton(SearchWin)
        self.searchButton.setText("Поиск")
        self.gridLayout.addWidget(self.searchButton, 1, 0, 1, 2)
        icon = QtGui.QIcon("search1.png")
        SearchWin.setWindowIcon(icon)
        self.cancelButton = QtWidgets.QPushButton(SearchWin)
        self.cancelButton.setText("Отмена")
        self.gridLayout.addWidget(self.cancelButton, 2, 0, 1, 2)