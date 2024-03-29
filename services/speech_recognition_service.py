import speech_recognition as speech_rec
import threading 

clouser_change_text = None
is_recording = False
recognizer = None
microphone = None

# speech_rec.Microphone.list_microphone_names() 

def audio_hadler(audio):
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print("TEXT --->", text)
        clouser_change_text(text)
    except:
        print("Error read text!!!")

def microphone_handler():
    while is_recording:
        with microphone as source: 
            print("MIC:", microphone, "SOURCE:", source)
            recognizer.adjust_for_ambient_noise(source) 
            audio = recognizer.listen(source) 
            print("AUDIO DATA", audio)
            thread = threading.Thread(target=audio_hadler(audio))
            thread.start()

def start():
    global is_recording, recognizer, microphone
    is_recording = True
    recognizer = speech_rec.Recognizer()
    microphone = speech_rec.Microphone()
    thread = threading.Thread(target=microphone_handler())
    thread.start()

def stop():
    global is_recording, recognizer, microphone
    is_recording = False
    recognizer = None
    microphone = None
