import pytest
from src.classifier import classify
from src.reader import Email, parse_email

@pytest.mark.parametrize('body, expected', [('Работа остановлена, ошибка 500', 'critical'),
                                            ('Не смог зайти на сайт, ошибка error', 'problem'),
                                            ('Мне нужны права доступа к сайту', 'access'),
                                            ('Объявление: конференция завтра', 'info'),
                                            ('Завтра на работе появится новый сотрудник', 'miss'),
                                            ('Прошу срочно перейти по ссылке', 'spam')])
def test_classify_categories(body, expected):
    email = Email(filename='test.txt', body=body)
    assert classify(email) == expected

def test_classify_other():
    email = Email(filename='test.txt', subject='Привет', body='Просто хотел узнать как дела')
    assert classify(email) == 'other'

def test_classify_unreadable():
    email = Email(filename='test.txt', is_readable=False)
    assert classify(email) == 'unreadable'

def test_classify_empty():
    email = Email(filename='test.txt')
    assert classify(email) == 'other'

def test_parse_normal_email(tmp_path):
    file = tmp_path / 'test_mail.txt'
    file.write_text('From: ivan@test.ru\nTo: support@company.ru\nSubject: Тестовая тема\n\nТело тестового письма',
                    encoding='utf-8')
    email = parse_email(str(file))
    assert email.sender == 'ivan@test.ru'
    assert email.recipient == 'support@company.ru'
    assert email.subject == 'Тестовая тема'
    assert email.body == 'Тело тестового письма'
    assert email.is_readable == True

def test_parse_empty_file(tmp_path):
    file = tmp_path / 'empty.txt'
    file.write_text('', encoding='utf-8')
    email = parse_email(str(file))
    assert email.is_readable == False

def test_parse_wrong_format(tmp_path):
    file = tmp_path / 'test.json'
    file.write_text('{"from": "test"}', encoding='utf-8')
    email = parse_email(str(file))
    assert email.is_readable == False