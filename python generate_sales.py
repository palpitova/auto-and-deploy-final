import csv
import os
import random
import uuid
from datetime import datetime

# Конфигурация
OUTPUT_DIR = 'data'
NUM_SHOPS = 5  # Количество магазинов для генерации
MAX_CASH_REGISTERS = 3  # Максимум касс в одном магазине
MIN_RECEIPTS_PER_FILE = 10  # Минимум чеков в одной выгрузке
MAX_RECEIPTS_PER_FILE = 50  # Максимум чеков в одной выгрузке
MAX_ITEMS_PER_RECEIPT = 5   # Максимум позиций в одном чеке

# База данных товаров для генерации (Категория -> Список товаров)
PRODUCT_DB = {
    "Бытовая химия": [
        ("Средство для мытья посуды", 150.00),
        ("Стиральный порошок 3кг", 450.50),
        ("Кондиционер для белья", 220.00),
        ("Средство для чистки стекол", 120.00),
        ("Таблетки для посудомойки", 800.00)
    ],
    "Текстиль": [
        ("Полотенце махровое", 350.00),
        ("Комплект постельного белья", 2500.00),
        ("Плед флисовый", 900.00),
        ("Скатерть", 600.00)
    ],
    "Кухонная утварь": [
        ("Сковорода с антипригарным покрытием", 1800.00),
        ("Набор ножей", 1200.00),
        ("Кастрюля эмалированная", 950.00),
        ("Форма для выпечки", 450.00),
        ("Чайник заварочный", 700.00)
    ],
    "Мелкая бытовая техника": [
        ("Блендер погружной", 2100.00),
        ("Тостер", 1500.00),
        ("Весы кухонные", 800.00)
    ]
}

def generate_doc_id():
    """Генерирует уникальный ID чека."""
    return uuid.uuid4().hex[:12].upper()

def get_random_product():
    """Возвращает случайный товар, его категорию и базовую цену."""
    category = random.choice(list(PRODUCT_DB.keys()))
    item_name, base_price = random.choice(PRODUCT_DB[category])
    return category, item_name, base_price

def generate_csv_files(num_shops):
    # Создаем папку data, если её нет
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Папка '{OUTPUT_DIR}' создана.")

    total_files = 0

    print("Начинаю генерацию файлов...")

    for shop_num in range(1, num_shops + 1):
        # Случайное кол-во касс в магазине (от 1 до N)
        num_registers = random.randint(1, MAX_CASH_REGISTERS)

        for cash_num in range(1, num_registers + 1):
            filename = f"{shop_num}_{cash_num}.csv"
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['doc_id', 'item', 'category', 'amount', 'price', 'discount']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                # Генерируем случайное количество чеков для этой кассы
                num_receipts = random.randint(MIN_RECEIPTS_PER_FILE, MAX_RECEIPTS_PER_FILE)

                for _ in range(num_receipts):
                    current_doc_id = generate_doc_id()
                    
                    # Генерируем позиции в чеке
                    num_items = random.randint(1, MAX_ITEMS_PER_RECEIPT)
                    
                    for _ in range(num_items):
                        category, item, base_price = get_random_product()
                        
                        # Генерация параметров продажи
                        amount = random.randint(1, 3) # Кол-во товара
                        
                        # Небольшой разброс цены
                        price = round(base_price * random.uniform(0.95, 1.05), 2)
                        
                        # Скидка с вероятностью 30%
                        discount = 0
                        if random.random() < 0.3:
                            # Скидка от 5% до 20% от суммы позиции
                            discount_val = (price * amount) * random.uniform(0.05, 0.20)
                            discount = round(discount_val, 2)

                        writer.writerow({
                            'doc_id': current_doc_id,
                            'item': item,
                            'category': category,
                            'amount': amount,
                            'price': price,
                            'discount': discount
                        })
            
            total_files += 1
            
    print(f"Готово! Сгенерировано {total_files} файлов в папке '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    generate_csv_files(NUM_SHOPS)
