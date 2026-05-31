import os
from src.reader import parse_email
from src.classifier import classify
import shutil

categories = ['critical', 'problem', 'access', 'info', 'miss', 'spam', 'other', 'unreadable']
for category in categories:
    category_path = os.path.join('classified', category)
    os.makedirs(category_path, exist_ok=True)

with open('log.txt', 'w', encoding='utf-8') as log:
    counter = {'critical': 0, 'problem': 0, 'access': 0, 'info': 0,
               'miss': 0, 'spam': 0, 'other': 0, 'unreadable': 0}
    for filename in sorted(os.listdir('inbox')):
        try:
            path = os.path.join('inbox', filename)
            email = parse_email(path)
            category = classify(email)
            dest = os.path.join('classified', category, filename)
            shutil.move(path, dest)
            if category == 'critical':
                log.write(f'{filename} -> {category} (Критический инцидент)\n')
                counter['critical'] += 1
            elif category == 'problem':
                log.write(f'{filename} -> {category} (Стандартная проблема)\n')
                counter['problem'] += 1
            elif category == 'access':
                log.write(f'{filename} -> {category} (Запрос доступа)\n')
                counter['access'] += 1
            elif category == 'info':
                log.write(f'{filename} -> {category} (Информация)\n')
                counter['info'] += 1
            elif category == 'miss':
                log.write(f'{filename} -> {category} (Сообщение не по адресу)\n')
                counter['miss'] += 1
            elif category == 'spam':
                log.write(f'{filename} -> {category} (Нежелательное содержимое)\n')
                counter['spam'] += 1
            elif category == 'other':
                log.write(f'{filename} -> {category} (Не совпало ни с одной категорией)\n')
                counter['other'] += 1
            elif category == 'unreadable':
                log.write(f'{filename} -> {category} (Письмо в неверном формате)\n')
                counter['unreadable'] += 1
        except Exception:
            log.write(f'{filename} -> ОШИБКА обработки\n')
    for category, count in counter.items():
        log.write(f'{category}: {count}\n')
    log.write(f'Всего обработано: {sum(counter.values())}')