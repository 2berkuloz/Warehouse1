from PyQt6 import QtCore, QtGui, QtWidgets

class EditWindow(QtWidgets.QWidget):
    editProductSignal = QtCore.pyqtSignal(int, str, str, str, str, str, str)

    def __init__(self, row, name, category, product_id, quantity, size, dimensions, categories):
        super().__init__()
        self.row = row
        self.ui = Ui_EditWindow(categories)
        self.ui.setupUi(self)
        self.ui.nameLineEdit.setText(name)
        self.ui.categoryComboBox.setCurrentText(category)
        self.ui.idLineEdit.setText(product_id)
        self.ui.quantityLineEdit.setText(quantity)
        self.ui.sizeLineEdit.setText(size)
        self.ui.dimensionsLineEdit.setText(dimensions)
        self.ui.editButton.clicked.connect(self.emitEditProductSignal)

    def emitEditProductSignal(self):
        category = self.ui.categoryComboBox.currentText()
        name = self.ui.nameLineEdit.text()
        product_id = self.ui.idLineEdit.text()
        quantity = self.ui.quantityLineEdit.text()
        size = self.ui.sizeLineEdit.text()
        dimensions = self.ui.dimensionsLineEdit.text()
        self.editProductSignal.emit(self.row, category, name, product_id, quantity, size, dimensions)
        self.close()


class Ui_EditWindow(object):
    def __init__(self, categories):
        self.categories = categories

    def setupUi(self, EditWindow):
        EditWindow.setWindowTitle("Редактировать")
        icon = QtGui.QIcon("edit3.png")
        EditWindow.setWindowIcon(icon)
        EditWindow.setObjectName("EditWindow")
        EditWindow.resize(400, 400)
        self.gridLayout = QtWidgets.QGridLayout(EditWindow)
        self.gridLayout.setObjectName("gridLayout")

        self.categoryLabel = QtWidgets.QLabel(EditWindow)
        self.categoryLabel.setText("Категория:")
        self.gridLayout.addWidget(self.categoryLabel, 0, 0, 1, 1)

        self.categoryComboBox = QtWidgets.QComboBox(EditWindow)
        self.categoryComboBox.addItems(self.categories)
        self.gridLayout.addWidget(self.categoryComboBox, 0, 1, 1, 1)

        self.nameLabel = QtWidgets.QLabel(EditWindow)
        self.nameLabel.setText("Наименование:")
        self.gridLayout.addWidget(self.nameLabel, 1, 0, 1, 1)
        self.nameLineEdit = QtWidgets.QLineEdit(EditWindow)
        self.gridLayout.addWidget(self.nameLineEdit, 1, 1, 1, 1)

        self.idLabel = QtWidgets.QLabel(EditWindow)
        self.idLabel.setText("ID:")
        self.gridLayout.addWidget(self.idLabel, 2, 0, 1, 1)
        self.idLineEdit = QtWidgets.QLineEdit(EditWindow)
        self.gridLayout.addWidget(self.idLineEdit, 2, 1, 1, 1)

        self.quantityLabel = QtWidgets.QLabel(EditWindow)
        self.quantityLabel.setText("Количество:")
        self.gridLayout.addWidget(self.quantityLabel, 3, 0, 1, 1)
        self.quantityLineEdit = QtWidgets.QLineEdit(EditWindow)
        self.gridLayout.addWidget(self.quantityLineEdit, 3, 1, 1, 1)

        self.sizeLabel = QtWidgets.QLabel(EditWindow)
        self.sizeLabel.setText("Размер:")
        self.gridLayout.addWidget(self.sizeLabel, 4, 0, 1, 1)
        self.sizeLineEdit = QtWidgets.QLineEdit(EditWindow)
        self.gridLayout.addWidget(self.sizeLineEdit, 4, 1, 1, 1)

        self.dimensionsLabel = QtWidgets.QLabel(EditWindow)
        self.dimensionsLabel.setText("Габариты:")
        self.gridLayout.addWidget(self.dimensionsLabel, 5, 0, 1, 1)
        self.dimensionsLineEdit = QtWidgets.QLineEdit(EditWindow)
        self.gridLayout.addWidget(self.dimensionsLineEdit, 5, 1, 1, 1)

        self.editButton = QtWidgets.QPushButton(EditWindow)
        self.editButton.setText("Редактировать")
        self.gridLayout.addWidget(self.editButton, 6, 0, 1, 2)