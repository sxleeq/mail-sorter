import os
from src.reader import parse_email
from src.classifier import classify
import shutil

categories = ['critical', 'problem', 'access', 'info', 'miss', 'spam', 'other', 'unreadable']
for category in categories:
    category_path = os.path.join('classified', category)
    os.makedirs(category_path, exist_ok=True)

for filename in sorted(os.listdir('inbox')):
    path = os.path.join('inbox', filename)
    email = parse_email(path)
    category = classify(email)
    print(f'{filename} => {category}')
    dest = os.path.join('classified', category, filename)
    shutil.move(path, dest)