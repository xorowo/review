import streamlit as st
import phonenumbers
import json
from os import path

#Проверка длины номера телефона
def check_len_pgone(phone):
    is_valid = not len(phone) < 12
    if not is_valid:
        st.warning("Некорректная длина номера телефона")
    return is_valid

#Проверка формата номера телефона
def check_format_phone(phone):
    try:
        my_number = phonenumbers.parse(phone, "RUS")
        is_valid = phonenumbers.is_valid_number(my_number)
        if not is_valid:
            st.warning("Некорректный формат номера телефона")
        return is_valid
    except phonenumbers.phonenumberutil.NumberParseException:
        st.warning("Некорректный формат номера телефона")
        return False

#Проверка длины отзыва
def check_len_review(review):
    is_valid = not len(review) < 30
    if not is_valid:
        st.warning("Минимальная длина отзыва 30 символов")
    return is_valid

#Проверка валидности формы
def check_valid_form(phone, review):
    is_valid = check_len_pgone(phone) and check_format_phone(phone) and check_len_review(review)
    return is_valid

#Запись в json файл
def write_to_json(review_dict_new):
    file_name = "data/reviews.json"
    review_dict = []
    
    if path.isfile(file_name):
        with open(file_name) as read_file:
            review_dict = json.load(read_file)

    review_dict.append(review_dict_new)

    with open(file_name, "w") as write_file:
        json.dump(review_dict, write_file, indent=4, separators=(',', ': '))

#Отчистка формы
def clear_form():
    st.session_state.input_phone_key = "+7"
    st.session_state.input_review_key = ""

#Проверка и запись формы
def send_form():
    phone = st.session_state.input_phone_key
    review = st.session_state.input_review_key

    if check_valid_form(phone, review):
        dictionary = {"phone": phone, "review": review}
        write_to_json(dictionary)
        clear_form()
        st.success("Отзыв отправлен.")

#Форма
with st.form("review_form"):
    phone_val = st.text_input(
        "Номер телефона",
        max_chars=12,
        value="+7",
        key="input_phone_key"
    )
    
    review_val = st.text_area(
        "Отзыв",
        max_chars=1000,
        key="input_review_key"
    )

    submit = st.form_submit_button(
        "Отправить",
        on_click=send_form
    )


