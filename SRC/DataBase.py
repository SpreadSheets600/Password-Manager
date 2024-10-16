import sqlite3
from Exceptions import DatabaseError

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('passwords.db')
        self.create_table()

    def create_table(self):
        try:
            with self.conn:
                self.conn.execute('''CREATE TABLE IF NOT EXISTS passwords (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    website TEXT NOT NULL,
                                    email TEXT NOT NULL,
                                    username TEXT NOT NULL,
                                    password TEXT NOT NULL
                                    );''')
        except sqlite3.Error as e:
            raise DatabaseError(f"Database error: {e}")

    def save_data(self, website, email, username, password):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO passwords (website, email, username, password) VALUES (?, ?, ?, ?)",
                                  (website, email, username, password))
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to save data: {e}")

    def get_all_passwords(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT website, email, username, password FROM passwords")
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to retrieve data: {e}")
