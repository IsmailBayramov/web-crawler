import sqlite3

def init_db():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('links1.db')
    cursor = connection.cursor()

    # Создаем таблицу Users
    cursor.execute('''CREATE TABLE IF NOT EXISTS Links (uri TEXT NOT NULL UNIQUE)''')
    return connection


def add_link(connection, uri):
    cursor = connection.cursor()
    cursor.execute('INSERT OR IGNORE INTO links (uri) VALUES (?)', (uri,))

    # Сохраняем изменения
    connection.commit()

def is_link_visited(connection, uri):
    cursor = connection.cursor()
    cursor.execute('SELECT 1 FROM links WHERE uri = ?', (uri,))
    return cursor.fetchone() is not None
