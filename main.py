import streamlit as st
import services.validate_service as validate
import services.database_service as database
import services.image_service as image
# import services.speech_recognition_service as recognition

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

st_empty_for_area = None

st.set_page_config(
    page_title="FeedbackAI",
    page_icon="📨"
)

st.image(image.get("logo.jpg"))
st.markdown("<h2 style='text-align: center;'>Ваш голос важен для нас!</h2>", unsafe_allow_html=True)
st.markdown("""FeedbackAI - это ваша возможность поделиться своим мнением о наших продуктах и услугах. Просто введите свой номер телефона и оставьте отзыв. Ваше мнение поможет нам стать еще лучше!""")

if "recognitioned_text" not in st.session_state:
    st.session_state.recognitioned_text = ""

def set_desc_text(text):
    st.session_state.recognitioned_text += " " + text
    st_empty_for_area.text_area(
        "Отзыв",
        st.session_state.recognitioned_text,
        max_chars=1000
    )

# recognition.clouser_change_text = set_desc_text
# recognition.ctx = st.runtime.scriptrunner.get_script_run_ctx()

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
    st.session_state.recognitioned_text = ""

#Проверка и отправка данных формы
def send_form():
    phone = st.session_state.input_phone_key
    review = st.session_state.recognitioned_text
    if is_valid_form(phone, review):
        dictionary = {"phone": phone, "review": review}
        response = database.insert(dictionary)
        if response["success"]:
            clear_form()
            st.success("Отзыв отправлен")
        else:
            st.warning("Error: {}".format(response["error"]))

stt_button = Button(label="Speak", width=100)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

if not "input_phone_key" in st.session_state:
    st.session_state.input_phone_key = "+7"

if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

webrtc_ctx = None

def record_button_click():
    st.session_state.is_recording = not st.session_state.is_recording

#Форма
with st.form("review_form"):
    st.text_input(
        "Номер телефона",
        max_chars=12,
        key="input_phone_key"
    )
    st_empty_for_area = st.empty()
    st_empty_for_area.text_area(
        "Отзыв",
        st.session_state.recognitioned_text,
        max_chars=1000
    )
    c1, c2 = st.columns(2)
    c1.form_submit_button(
        "Отправить",
        on_click=send_form
    )

    # c2_empty = c2.empty()
    # if st.session_state.is_recording:
    #     c2_empty.form_submit_button(
    #         "Остановить",
    #         on_click=record_button_click
    #     )
    #     recognition.start()
    # else:
    #     c2_empty.form_submit_button(
    #         "Запись",
    #         on_click=record_button_click
    #     )
    #     recognition.stop() 

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        text = result.get("GET_TEXT")
        set_desc_text(text)





