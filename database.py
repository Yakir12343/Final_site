import sqlite3
from fileinput import close


class Database:
    def __init__(self):
        self.database_way = "sqlite.db"


    def get_connection(self):
        connection = sqlite3.connect(self.database_way)  # Новое соединение
        connection.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        return connection

    def close(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            if cursor is not None:
                cursor.close()
        finally:
            connection.close()


    def create_table(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        '''
        cursor.execute(query)
        connection.commit()
        close()

    def register(self, username, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = '''
            INSERT INTO users (username, password) VALUES (?, ?)
        '''
        args = (username, password)
        cursor.execute(query, args)
        connection.commit()
    
    def login(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = '''
            SELECT * FROM users WHERE username = ?
        '''
        args = (username,)
        user = cursor.execute(query, args).fetchone()
        connection.commit()
        return user