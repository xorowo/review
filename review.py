import streamlit as st
import review_validate as validate
import review_db as db

#Проверка валидности формы
def is_valid_form(phone, review):
    if not validate.is_valid_len_phone(phone):
        st.warning("Некорректная длина номера телефона")
        return False
    if not validate.is_valid_format_phone(phone):
        st.warning("Некорректный формат номера телефона")
        return False
    if not validate.is_valid_len_review(review):
        st.warning("Отзыв пустой")
        return False
    return True

#Отчистка формы
def clear_form():
    st.session_state.input_phone_key = "+7"
    st.session_state.input_review_key = ""

#Проверка и отправка данных формы
def send_form():
    phone = st.session_state.input_phone_key
    review = st.session_state.input_review_key

    if is_valid_form(phone, review):
        dictionary = {"phone": phone, "review": review}
        response = db.insert(dictionary)
        if response["success"]:
            clear_form()
            st.success("Отзыв отправлен")
        else:
            st.warning("Error: {}".format(response["error"]))

st.session_state.input_phone_key = "+7"

#Форма
with st.form("review_form"):
    phone_val = st.text_input(
        "Номер телефона",
        max_chars=12,
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




