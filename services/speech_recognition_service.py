import speech_recognition as speech_rec
import pyaudio
import wave
import threading 

from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

CHUNK = 1024 # определяет форму ауди сигнала
FRT = pyaudio.paInt16 # шестнадцатибитный формат задает значение амплитуды
CHAN = 1 # канал записи звука
RT = 44100 # частота 
REC_SEC = 5 #длина записи
OUTPUT = "output.wav"

clouser_change_text = None

stream = None
stream_data_list = []
audio = None 

threads = []

is_recording = False

def write_to_file():
    w = wave.open(OUTPUT, 'wb')
    w.setnchannels(CHAN)
    w.setsampwidth(audio.get_sample_size(FRT))
    w.setframerate(RT)
    w.writeframes(b''.join(stream_data_list))
    w.close()

def read_from_file():
    samples = speech_rec.WavFile('output.wav')
    recognizer = speech_rec.Recognizer()
    with samples as sample:
        content = recognizer.record(sample)
        recognizer.adjust_for_ambient_noise(sample)
        try:
            text = recognizer.recognize_google(content, language="ru-RU")
            clouser_change_text(text)
        except:
            print("Error read text!!!")

def loop_handler():
    count = int(RT / CHUNK)
    while is_recording:
        print("LOOP HANDLER")
        for i in range(count):
            stream_data = stream.read(CHUNK)
            stream_data_list.append(stream_data)
        # th_2 = threading.Thread(target=write_and_read_file)
        # threads.append(th_2)
        # # add_script_run_ctx(th_2, get_script_run_ctx())
        # th_2.start()

def write_and_read_file():
    write_to_file()
    read_from_file()

def loop_write_and_read_file():
    while is_recording:
        print("LOOP WRITE AND READ FILE")
        write_to_file()
        read_from_file()

def start():
    global stream, audio, is_recording
    is_recording = True
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FRT,channels=CHAN,rate=RT,input=True,frames_per_buffer=CHUNK)

    th_1 = threading.Thread(target=loop_handler)
    threads.append(th_1)
    # add_script_run_ctx(th_1, get_script_run_ctx())
    th_1.start()

    th_2 = threading.Thread(target=loop_write_and_read_file())
    threads.append(th_2)
    th_2.start()


def stop():
    global is_recording
    is_recording = False
    if stream:
        [thread.join() for thread in threads]
        # th_2 = threading.Thread(target=read_from_file())
        # threads.append(th_2)
        # th_2.start()
        # th_2.join()
        stream.stop_stream() 
        stream.close()
        audio.terminate()
