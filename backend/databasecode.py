import sqlite3

def connect_db():
  connection = sqlite3.connect('universities.db')
  return connection

def create_table():
  connection = connect_db()
  cursor = connection.cursor()

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS universities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    link TEXT,
    qs INTEGER
  )
  ''')

  connection.commit()
  connection.close()

create_table()
connection = connect_db()
cursor = connection.cursor()
record_count = cursor.execute("SELECT COUNT(*) FROM universities").fetchone()[0]
connection.close()


def save_data(name, url, qs):
  connection = connect_db()
  cursor = connection.cursor()
  new_data_counter = 0
  global record_count

  cursor.execute("SELECT * FROM universities WHERE link = ?", (url,))
  existing = cursor.fetchone()

  if not existing:
    cursor.execute('''INSERT INTO universities (name, link, qs)
                      VALUES (?, ?, ?)''', (name, url, qs))
    connection.commit()
    new_data_counter += 1
    record_count += 1

  connection.close()
  return new_data_counter


def get_all_data():
  connection = connect_db()
  cursor = connection.cursor()

  cursor.execute("SELECT name, link, qs FROM universities")
  universities = cursor.fetchall()

  connection.close()
  global record_count
  return universities, record_count

def clear_all_data():
  connection = connect_db()
  cursor = connection.cursor()

  cursor.execute("DELETE FROM universities")  # Очищаем все записи из таблицы universities

  connection.commit()
  connection.close()
  global record_count
  record_count = 0

def get_record_count():
  global record_count
  return record_count

def print_all_data():
    connection = connect_db()
    cursor = connection.cursor()
    
    # Выполняем запрос для получения всех данных из таблицы
    cursor.execute("SELECT * FROM universities")
    
    # Получаем все строки
    rows = cursor.fetchall()
    
    # Проверяем, есть ли данные в таблице
    if rows:
        for row in rows:
            print(row)  # Выводим каждую строку на консоль
    else:
        print("Таблица пуста.")
    
    connection.close()

def get_universities_with_ranks():
  try:
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT name, link, qs FROM universities')
    universities = cursor.fetchall()
    connection.close()
    return universities, len(universities)
  except Exception as e:
    print(f"Ошибка при извлечении данных: {e}")
    return [], 0
