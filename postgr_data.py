import os
import csv
import re
import psycopg2
from psycopg2 import extras

# Конфигурация
DATA_DIR = 'data'

# Настройки подключения к PostgreSQL
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'      # Имя вашей базы данных
DB_USER = 'postgres'      # Ваш пользователь (обычно postgres)
DB_PASS = 'ваш_пароль'    # Впишите сюда пароль

# Имя целевой таблицы
TABLE_NAME = 'data_shops'

# Регулярное выражение: shop_id (цифры) _ cash_id (цифры) .csv
FILENAME_PATTERN = re.compile(r'^(\d+)_(\d+)\.csv$')

def get_db_connection():
    """Создает подключение к базе данных."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

def process_files():
    if not os.path.exists(DATA_DIR):
        print(f"Ошибка: Папка '{DATA_DIR}' не найдена.")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("Подключение к PostgreSQL успешно.")

        files_processed = 0
        rows_inserted = 0

        # Перебираем файлы
        for filename in os.listdir(DATA_DIR):
            match = FILENAME_PATTERN.match(filename)
            if not match:
                continue

            shop_id = int(match.group(1))
            cash_id = int(match.group(2))
            filepath = os.path.join(DATA_DIR, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    
                    to_insert = []
                    for row in reader:
                        # Подготовка строки. Обратите внимание:
                        # Postgres требует %s, данные передаются кортежем.
                        to_insert.append((
                            row['doc_id'],
                            shop_id,
                            cash_id,
                            row['item'],
                            row['category'],
                            int(row['amount']),
                            float(row['price']),
                            float(row['discount'])
                        ))

                    if to_insert:
                        # ИСПОЛЬЗУЕМ execute_values ДЛЯ СКОРОСТИ
                        # Это генерирует один запрос: INSERT INTO ... VALUES (...), (...), ...
                        query = f"""
                            INSERT INTO {TABLE_NAME} 
                            (doc_id, shop_id, cash_id, item_name, category, amount, price, discount)
                            VALUES %s
                        """
                        extras.execute_values(cursor, query, to_insert)
                        
                        conn.commit() # Фиксируем транзакцию после каждого файла
                        rows_inserted += len(to_insert)
                        files_processed += 1
                        print(f"Обработан файл: {filename} ({len(to_insert)} строк)")

            except Exception as e:
                print(f"Ошибка при чтении файла {filename}: {e}")
                conn.rollback() # Откат текущей транзакции при ошибке

        print("-" * 30)
        print(f"Итог: Обработано файлов: {files_processed}. Добавлено записей: {rows_inserted}.")

    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
    finally:
        if conn:
            conn.close()
            print("Соединение с БД закрыто.")

if __name__ == "__main__":
    process_files()
