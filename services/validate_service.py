import re

#Проверка длины номера телефона
def is_valid_len_phone(phone):
    is_valid = not len(phone) < 12
    return is_valid

#Проверка формата номера телефона
def is_valid_format_phone(phone):
    expression = re.compile(r"^((\+7|7|8)+([0-9]){10})$")
    return re.fullmatch(expression, phone)

#Проверка отзыва на пустоту
def is_valid_len_review(review):
    is_valid = review
    return is_valid
