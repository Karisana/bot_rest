import sqlite3


class Database:
    """Класс для работы с БД телеграм бота"""

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        """Проверяет наличие пользователя в бд"""
        with self.connection:
            res = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchmany(1)
            return bool(len(res))

    def add_user(self, user_id):
        """Добавляет пользователя в бд"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

    def set_active(self, user_id, active):
        """Активность пользователя в бд: 1 - активный, 0 - не активный"""
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'active' = ? WHERE 'user_id' = ?", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM 'users'").fetchall()

