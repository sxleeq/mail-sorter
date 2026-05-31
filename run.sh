#!/bin/bash
echo 'Начинаю обработку писем'
if [ -d 'inbox' ]; then
    python3 main.py
else
    echo 'Папки inbox нету'
fi
echo 'Обработка завершена'