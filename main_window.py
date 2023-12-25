from PyQt6 import QtCore, QtGui, QtWidgets
from database import Database
from edit_window import EditWindow
from add_window import AddWindow
from search_window import SearchWindow
import sys
import random

class Ui_MainWindow(object):
    COLUMN_COUNT = 6

    ICON_PATHS = {
        'add': 'add1.png',
        'edit': 'edit3.png',
        'delete': 'delete1.png',
        'search': 'search1.png',
        'save': 'save.png',
        'load': 'load.png',
    }

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1060, 650)
        MainWindow.setWindowTitle("Твой склад")
        icon = QtGui.QIcon("icon.png")
        MainWindow.setWindowIcon(icon)

        self.setupTableWidget(MainWindow)
        self.setupButtons(MainWindow)
        self.setupDatabase()
        

    def setupTableWidget(self, MainWindow):
        self.tableWidget = QtWidgets.QTableWidget(parent=MainWindow)
        self.tableWidget.setGeometry(QtCore.QRect(30, 100, 981, 451))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(Ui_MainWindow.COLUMN_COUNT)
        header_labels = ["Категория", "Наименование товара", "ID", "Количество", "Размер", "Габариты"]
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(0, 150)

    def setupButtons(self, MainWindow):
        self.addButton = self.createButton(MainWindow, 'add', self.openAddWindow, 35, 30)
        self.editButton = self.createButton(MainWindow, 'edit', self.openEditWindow, 110, 30)
        self.deleteButton = self.createButton(MainWindow, 'delete', self.deleteRow, 175, 30)
        self.searchButton = self.createButton(MainWindow, 'search', self.openSearchWindow, 240, 30)
        self.saveButton = self.createButton(MainWindow, 'save', self.show_save_confirmation, 880, 560)
        self.loadButton = self.createButton(MainWindow, 'load', self.show_load_confirmation, 950, 560)

    def createButton(self, parent, icon_name, slot, x, y):
        button = QtWidgets.QPushButton(parent=parent)
        button.setGeometry(QtCore.QRect(x, y, 70, 70))
        button.setIcon(QtGui.QIcon(Ui_MainWindow.ICON_PATHS.get(icon_name, '')))
        button.setIconSize(QtCore.QSize(60, 60))
        button.setFlat(True)
        button.clicked.connect(slot)
        return button

    def sortByColumn(self, logicalIndex):
        currentOrder = self.tableWidget.horizontalHeader().sortIndicatorOrder()
        if logicalIndex == 3:
            newOrder = (QtCore.Qt.SortOrder.DescendingOrder if currentOrder == QtCore.Qt.SortOrder.AscendingOrder
                        else QtCore.Qt.SortOrder.AscendingOrder)
            self.tableWidget.sortByColumn(logicalIndex, newOrder)
        else:
            self.tableWidget.sortByColumn(logicalIndex, QtCore.Qt.SortOrder.AscendingOrder)
        if logicalIndex != 3:
            header = self.tableWidget.horizontalHeader()
            header.setSortIndicator(-1, QtCore.Qt.SortOrder.AscendingOrder)

    def create_confirmation_box(self, text, title):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Question)
        icon = QtGui.QIcon("ask.png")
        msg_box.setWindowIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        return msg_box

    def setupDatabase(self):
        self.db = Database('products.db')
        self.db.create_table()

    def clear_table_visibility(self):
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(row, False)

    def generate_random_id(self):
        return ''.join(random.choice('0123456789') for _ in range(8))

    def id_exists(self, product_id):
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 2).text() == product_id:
                return True
        return False


    def save_to_database(self):
        self.db.clear_database()
        data = []
        for row in range(self.tableWidget.rowCount()):
            category = self.tableWidget.item(row, 0).text()
            name = self.tableWidget.item(row, 1).text()
            product_id = self.tableWidget.item(row, 2).text()
            quantity = self.tableWidget.item(row, 3).text()
            size_item = self.tableWidget.item(row, 4)
            size = size_item.text() if size_item else ""

            dimensions_item = self.tableWidget.item(row, 5)
            dimensions = dimensions_item.text() if dimensions_item else ""
            data.append((category, name, product_id, quantity, size, dimensions))

        self.db.save_to_database(data)
        self.show_message_box("Данные успешно сохранены в базу данных.")

    def show_save_confirmation(self):
        msg_box = self.create_confirmation_box(
            "Вы уверены, что хотите сохранить данные в базу данных?",
            "Подтвердите действие"
        )

        yes_button = msg_box.addButton("Да", QtWidgets.QMessageBox.ButtonRole.YesRole)
        msg_box.addButton("Нет", QtWidgets.QMessageBox.ButtonRole.NoRole)
        response = msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            self.save_to_database()
        else:
            self.show_message_box("Сохранение отменено.")

    def load_from_database(self):
        self.clear_table()
        data = self.db.load_from_database()
        for row_data in data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_position, column, item)

    def show_load_confirmation(self):
        msg_box = self.create_confirmation_box(
            "Вы уверены, что хотите загрузить данные из базы данных? Все текущие данные будут заменены.",
            "Подтвердите действие"
        )

        yes_button = msg_box.addButton("Да", QtWidgets.QMessageBox.ButtonRole.YesRole)
        msg_box.addButton("Нет", QtWidgets.QMessageBox.ButtonRole.NoRole)
        response = msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            self.load_from_database()
            self.show_message_box("Данные успешно загружены из базы данных.")
        else:
            self.show_message_box("Загрузка отменена.")

    def clear_table(self):
        self.tableWidget.setRowCount(0)

    def show_message_box(self, message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        icon = QtGui.QIcon("good.png")
        msg_box.setWindowIcon(icon)
        msg_box.setText(message)
        msg_box.setWindowTitle("Действие подтверждено")
        msg_box.exec()

    def deleteRow(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Question)
            msg_box.setText("Вы уверены, что хотите удалить эту строку(товар)?")
            msg_box.setWindowTitle("Удалить")
            icon = QtGui.QIcon("delete1.png")
            msg_box.setWindowIcon(icon)

            yes_button = msg_box.addButton("Да", QtWidgets.QMessageBox.ButtonRole.YesRole)
            msg_box.addButton("Нет", QtWidgets.QMessageBox.ButtonRole.NoRole)

            msg_box.exec()

            if msg_box.clickedButton() == yes_button:
                self.tableWidget.removeRow(selected_row)
                msg_boxyes = QtWidgets.QMessageBox()
                msg_boxyes.setWindowIcon(icon)
                msg_boxyes.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                msg_boxyes.setWindowTitle("Удалено.")
                msg_boxyes.setText("Строка (товар) успешно удалена.")
                msg_boxyes.exec()
        else:
            error_box = QtWidgets.QMessageBox()
            error_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_box.setText("Выберите строку(товар) для удаления.")
            error_box.setWindowTitle("Ошибка")
            error_icon = QtGui.QIcon("error.png")
            error_box.setWindowIcon(error_icon)
            error_box.exec()   
            
    def insert_row_from_data(self, row_data):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        for column, value in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(value))
            self.tableWidget.setItem(row_position, column, item)

    def openEditWindow(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            category_item = self.tableWidget.item(selected_row, 0)
            if category_item is not None:
                category = category_item.text()
                name = self.tableWidget.item(selected_row, 1).text()
                product_id = self.tableWidget.item(selected_row, 2).text()
                quantity = self.tableWidget.item(selected_row, 3).text()
                size_item = self.tableWidget.item(selected_row, 4)
                size = size_item.text() if size_item is not None else ""
                dimensions_item = self.tableWidget.item(selected_row, 5)
                dimensions = dimensions_item.text() if dimensions_item is not None else ""
                self.edit_window = EditWindow(selected_row, name, category, product_id, quantity, size, dimensions, self.db.get_categories())
                self.edit_window.editProductSignal.connect(self.editProductInTable)
                self.edit_window.show()
            else:
                error_box = QtWidgets.QMessageBox()
                error_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                error_icon = QtGui.QIcon("error.png")
                error_box.setWindowIcon(error_icon)
                error_box.setText("Выберите строку(товар) для редактирования.")
                error_box.setWindowTitle("Ошибка")
                error_box.exec()
        else:
            error_box = QtWidgets.QMessageBox()
            error_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_box.setText("Выберите строку(товар) для редактирования.")
            error_icon = QtGui.QIcon("error.png")
            error_box.setWindowIcon(error_icon)
            error_box.setWindowTitle("Ошибка")
            error_box.exec()

    def editProductInTable(self, row, category, name, product_id, quantity, size, dimensions):
        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(category))
        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
        self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(product_id))
        self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(quantity))
        self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(size))
        self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(dimensions))


    def openAddWindow(self):
        product_id = self.generate_random_id()
        categories = self.db.get_categories()
        self.add_window = AddWindow(product_id, self.db, categories)
        self.add_window.addProductSignal.connect(self.addProductToTable)
        self.add_window.show()

    def openSearchWindow(self):
        self.search_window = SearchWindow()
        self.search_window.show()
        self.search_window.searchProductSignal.connect(self.searchProductInTable)
        self.search_window.cancelSearchSignal.connect(self.clear_table_visibility)

    def searchProductInTable(self, search_term):
        self.clear_table_visibility()
        for row in range(self.tableWidget.rowCount()):
            item_category = self.tableWidget.item(row, 0)
            item_name = self.tableWidget.item(row, 1)
            item_id = self.tableWidget.item(row, 2)

            if item_category is not None and item_name is not None and item_id is not None:
                category_match = search_term.lower() in item_category.text().lower()
                name_match = search_term.lower() in item_name.text().lower()
                id_match = search_term.lower() in item_id.text().lower()

                if category_match or name_match or id_match:
                    self.tableWidget.showRow(row)
                else:
                    self.tableWidget.hideRow(row)

    def addProductToTable(self, category, name, product_id, quantity):
        if not self.id_exists(product_id):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(category))
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(name))
            self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(product_id))
            self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(quantity))
        else:
            self.show_message_box("Товар с таким ID уже существует.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    db = Database('products.db')
    db.create_category_table()

    categories_to_insert = []
    for category in categories_to_insert:
        db.insert_category(category)
    MainWindow.show()
    sys.exit(app.exec())