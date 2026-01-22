#!/bin/bash
cd "/Users/dariapolitova/Documents/Коды"
echo "- Запуск Импорта данных в PostgreSQL: $(date) ---" >> script_log.txt
/usr/bin/python3 postgr_data.py >> script_log.txt 2>&1
