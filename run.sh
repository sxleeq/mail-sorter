#!/bin/bash
echo 'начинаю обработку писем'
if [ -d 'inbox' ]; then
    python3 main.py
else
    echo 'папки inbox нет'
fi
echo 'обработка завершина'