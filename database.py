import sqlite3
from PyQt6 import QtCore

class Database:
    CATEGORY_TABLE_NAME = 'categories'
    CATEGORY_FIELDS = ['category_name']

    def __init__(self, db_path):
        """Инициализация объекта базы данных с подключением к указанному пути"""
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_category_table()

    def create_category_table(self):
        """Метод для создания таблицы категорий в базе данных"""
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.CATEGORY_TABLE_NAME} (
                {', '.join(f"{field} TEXT" for field in self.CATEGORY_FIELDS)}
            )
        ''')
        self.connection.commit()

    def insert_category(self, category_name):
        """Метод для вставки новой категории в таблицу категорий"""
        self.cursor.execute(f'''
            INSERT INTO {self.CATEGORY_TABLE_NAME} ({', '.join(self.CATEGORY_FIELDS)})
            VALUES (?)
        ''', (category_name,))
        self.connection.commit()

    def get_categories(self):
        """Метод для получения уникальных категорий из таблицы категорий"""
        self.cursor.execute(f'SELECT DISTINCT {", ".join(self.CATEGORY_FIELDS)} FROM {self.CATEGORY_TABLE_NAME}')
        categories = [row[0] for row in self.cursor.fetchall()]
        return categories
    
    def get_all_categories(self):
        self.cursor.execute(f'SELECT DISTINCT {", ".join(self.CATEGORY_FIELDS)} FROM {self.CATEGORY_TABLE_NAME}')
        categories = [result[0] for result in self.cursor.fetchall()]
        return categories

    def create_table(self):
        """Метод для создания таблицы продуктов в базе данных"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                category TEXT,
                name TEXT,
                product_id TEXT,
                quantity TEXT,
                size TEXT,
                dimensions TEXT
            )
        ''')
        self.connection.commit()
        print("Table 'products' created successfully.")

    def save_to_database(self, data):
        """Метод для сохранения данных в таблицу продуктов в базе данных"""
        self.cursor.executemany('''
            INSERT INTO products (category, name, product_id, quantity, size, dimensions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        self.connection.commit()

    def execute_query(self, query, params=None):
        """Метод для выполнения произвольного SQL-запроса"""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.connection.commit()

    def create_log_table(self):
        """Метод для создания таблицы лога событий"""
        query = """
        CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT,
            timestamp TEXT
        );
        """
        self.execute_query(query)

    def add_log_entry_to_database(self, entry):
        """Метод для добавления записи в таблицу лога"""
        timestamp = QtCore.QDateTime.currentDateTime().toString()
        query = "INSERT INTO log (entry, timestamp) VALUES (?, ?);"
        params = (entry, timestamp)
        self.execute_query(query, params)

    def load_log_from_database(self):
        """Метод для загрузки записей из таблицы лога"""
        query = "SELECT entry FROM log ORDER BY timestamp DESC;"
        self.cursor.execute(query)
        return [entry[0] for entry in self.cursor.fetchall()]

    def delete_log_entry(self, log_id):
        """Метод для удаления записи из таблицы лога по её идентификатору"""
        query = "DELETE FROM log WHERE id = ?;"
        self.execute_query(query, (log_id,))
        self.connection.commit()

    def load_from_database(self):
        """Метод для загрузки данных из таблицы продуктов"""
        self.cursor.execute('SELECT * FROM products')
        data = self.cursor.fetchall()
        return data
    
    def clear_database(self):
        """Метод для очистки таблицы продуктов"""
        query = "DELETE FROM products"
        self.cursor.execute(query)
        self.connection.commit()

    def close_connection(self):
        """Метод для закрытия соединения с базой данных"""
        self.connection.close()