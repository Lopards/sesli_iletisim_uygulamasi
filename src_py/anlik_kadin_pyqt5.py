from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from src_py.src_ui.anlik_kadin import Ui_AnlikKadn_window
import pyaudio
import numpy as np
from scipy import signal
import threading


class anlik_kadin_page(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.anlik_kadin = Ui_AnlikKadn_window()
        self.anlik_kadin.setupUi(self)

        self.anlik_kadin.pushButton_BaslatK.clicked.connect(self.ses_degisimi_baslat)
        self.anlik_kadin.pushButton_DurdurK.clicked.connect(self.ses_degisimi_durdur)



        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.PITCH_SHIFT_FACTOR = 0.8
        self.DELAY_SECONDS = 0 # Değişiklik: Delay süresi 0 saniye olarak ayarlandı

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_running = False
        self.is_paused = False
        self.is_gender_change_paused = False
        self.Thread = None
    
   

    def ses_degisimi_baslat(self):
        if self.Thread is None or not self.Thread.is_alive():
            self.Thread = threading.Thread(target=self.baslat_ses_degisimi)
            self.Thread.start()

    def ses_degisimi_durdur(self):
        self.is_running = False
        self.is_gender_change_paused = False
        self.Thread.join()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def baslat_ses_degisimi(self):
        self.is_running = True
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.CHUNK)

        kaydedilen_list = []
        while self.is_running:
            input_data = self.stream.read(self.CHUNK)
            kaydedilen_list.append(input_data)
            audio_data = np.frombuffer(input_data, dtype=np.float32) * 1.3

            
            kaydedilen_sinyal = np.frombuffer(b''.join(kaydedilen_list[-int(self.RATE / self.CHUNK * self.DELAY_SECONDS):]), dtype=np.int16)
            cinsiyet = self.classify_gender(kaydedilen_sinyal)

            if cinsiyet == "Erkek":
                    shifted_audio_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR))
                    self.stream.write(shifted_audio_data.tobytes())
            elif cinsiyet == "Kadın":
                    # Ses değiştirme fonksiyonuna girmeden doğrudan sesi yolla
                    self.stream.write(audio_data.tobytes())

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def classify_gender(self, audio_data):
        if np.mean(audio_data) > 0:
            gender = "Kadın"
        else:
            gender = "Erkek"
        return gender

