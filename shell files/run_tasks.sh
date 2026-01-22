#!/bin/bash
cd "/Users/dariapolitova/Documents/Коды"
echo "- Запуск Генерации данных: $(date) ---" >> script_log.txt
/usr/bin/python3 generate_sales.py >> script_log.txt 2>&1
