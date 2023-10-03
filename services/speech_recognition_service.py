import speech_recognition as speech_rec
import pyaudio
import threading 

clouser_change_text = None
is_recording = False
recognizer = None
microphone = None

# sr.Microphone.list_microphone_names() 

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
            recognizer.adjust_for_ambient_noise(source) 
            audio = recognizer.listen(source) 
            thread = threading.Thread(target=audio_hadler(audio))
            thread.start()

    # if not is_recording:
    #     return
    # with microphone as micro: 
    #     print("micro", micro)
    #     recognizer.adjust_for_ambient_noise(micro) 
    #     print("adjust_for_ambient_noise")
    #     audio = recognizer.listen(micro) 
    #     print("audio")
    #     thread = threading.Thread(target=audio_hadler(audio))
    #     thread.start()
    # microphone_handler()

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
