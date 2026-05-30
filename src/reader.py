from dataclasses import dataclass
import os

@dataclass
class Email:
    filename: str
    sender: str = ''
    recipient: str = ''
    subject: str = ''
    body: str = ''
    is_readable: bool = True

def read_file(path):
    try:
        with open(path, encoding='utf-8') as f:
            text = f.read()
        return text
    except (UnicodeDecodeError, OSError):
        return None

def find_field(lines, keys):
    for line in lines:
        for key in keys:
            if line.lower().startswith(key):
                return line.split(':', 1)[1].strip()
    return ''

def parse_email(path):
    filename = os.path.basename(path)
    text = read_file(path)
    if text is None:
        return Email(filename, is_readable=False)
    lines = text.splitlines()
    sender = find_field(lines, ['from:', 'от кого:', 'ot kogo:'])
    recipient = find_field(lines, ['to:', 'кому:', 'komu:'])
    subject = find_field(lines, ['subject:', 'тема:', 'tema:'])
    index = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == '':
            index = i
            break
    body = '\n'.join(lines[index + 1:])
    return Email(filename=filename, sender=sender, recipient=recipient, subject=subject, body=body, is_readable=True)