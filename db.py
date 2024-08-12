import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('links.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Links (
id INTEGER PRIMARY KEY AUTOINCREMENT,
uri TEXT NOT NULL UNIQUE
)
''')

def add_link(uri):
    # Устанавливаем соединение с базой данных
    cursor.execute('INSERT INTO Links VALUES (?, ?)', (None, uri))

    # Сохраняем изменения
    connection.commit()

def close_connection():
    # Закрываем соединение
    connection.close()
