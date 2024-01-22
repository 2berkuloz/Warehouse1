from PyQt6 import QtCore, QtGui, QtWidgets
from database import Database

class AddWindow(QtWidgets.QWidget):
    """Класс, отправляемый при добавлении нового продукта"""
    addProductSignal = QtCore.pyqtSignal(str, str, str, str)

    def __init__(self, product_id, db, categories):
        """Инициализация окна добавления товара"""
        super().__init__()
        self.product_id = product_id
        self.db = db
        self.ui = Ui_AddWindow(categories)
        self.ui.setupUi(self)
        self.ui.idLineEdit.setText(self.product_id)
        self.ui.addButton.clicked.connect(self.emitAddProductSignal)
        self.ui.addButtonCategory.clicked.connect(self.showAddCategoryDialog)

    def emitAddProductSignal(self):
        """Метод для отправки сигнала при добавлении товара"""
        category = self.ui.categoryComboBox.currentText()
        name = self.ui.nameLineEdit.text()
        quantity = self.ui.quantityLineEdit.text()
        self.addProductSignal.emit(self.product_id, category, name, quantity)
        self.close()

    def showAddCategoryDialog(self):
        """Метод для отображения диалогового окна добавления новой категории"""
        new_category, ok = QtWidgets.QInputDialog.getText(self, "Добавить категорию", "Введите название категории:")
        if ok and new_category:
            self.db.insert_category(new_category)
            categories = self.db.get_categories()
            self.ui.categoryComboBox.clear()
            self.ui.categoryComboBox.addItems(categories)
            self.ui.categoryComboBox.setCurrentText(new_category)

class Ui_AddWindow(object):
    def __init__(self, categories):
        """Инициализация интерфейса окна добавления товара"""
        self.categories = categories
        
    def setupUi(self, Form):
        """Метод для настройки интерфейса окна добавления товара"""
        Form.resize(400, 300)
        Form.setWindowTitle("Добавить товар")
        icon = QtGui.QIcon("add1.png")
        Form.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.categoryLabel = QtWidgets.QLabel(Form)
        self.categoryLabel.setText("Категория:")
        self.gridLayout.addWidget(self.categoryLabel, 0, 0, 1, 1)
        self.categoryComboBox = QtWidgets.QComboBox(Form)
        self.gridLayout.addWidget(self.categoryComboBox, 0, 1, 1, 1)
        self.categoryComboBox.clear()
        self.categoryComboBox.addItems(self.categories)
        self.nameLabel = QtWidgets.QLabel(Form)
        self.nameLabel.setText("Наименование:")
        self.gridLayout.addWidget(self.nameLabel, 1, 0, 1, 1)
        self.nameLineEdit = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.nameLineEdit, 1, 1, 1, 1)
        self.idLabel = QtWidgets.QLabel(Form)
        self.idLabel.setText("ID:")
        self.gridLayout.addWidget(self.idLabel, 2, 0, 1, 1)
        self.idLineEdit = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.idLineEdit, 2, 1, 1, 1)
        self.quantityLabel = QtWidgets.QLabel(Form)
        self.quantityLabel.setText("Количество:")
        self.gridLayout.addWidget(self.quantityLabel, 3, 0, 1, 1)
        self.quantityLineEdit = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.quantityLineEdit, 3, 1, 1, 1)
        self.addButtonCategory = QtWidgets.QPushButton(Form)
        self.addButtonCategory.setText("Добавить категорию")
        self.gridLayout.addWidget(self.addButtonCategory, 0, 2, 1, 2)
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setText("Добавить товар")
        self.gridLayout.addWidget(self.addButton, 4, 0, 1, 2)