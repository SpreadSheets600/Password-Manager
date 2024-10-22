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
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT website, email, username, password FROM passwords")
                results = cursor.fetchall()
                return results if results else [] 
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to retrieve data: {e}")

    def update_password(self, old_data, new_data):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    """
                    UPDATE passwords 
                    SET website = ?, email = ?, username = ?, password = ?
                    WHERE website = ? AND email = ? AND username = ? AND password = ?
                    """,
                    (new_data['website'], new_data['email'], new_data['username'], new_data['password'],
                    old_data[0], old_data[1], old_data[2], old_data[3])
                )
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to update password: {e}")

    def search_passwords(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT website, email, username, password FROM passwords WHERE website LIKE ? OR email LIKE ?", 
                           (f'%{query}%', f'%{query}%'))
            results = cursor.fetchall()
            return results if results else []  
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to retrieve data: {e}")

    def delete_password(self, data):
        try:
            with self.conn:
                self.conn.execute("DELETE FROM passwords WHERE website = ? AND email = ? AND username = ? AND password = ?", data)
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to delete data: {e}")

    def __del__(self):

        if self.conn:
            self.conn.close()
