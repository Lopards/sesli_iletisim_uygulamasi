from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from src_py.src_ui.ses_kaydi import  Ui_Ses_kaydi_window

import pyaudio
import numpy as np
import soundfile as sf

class sound_record_page(QWidget):
    def __init__(self) -> None:
        super().__init__()
    
        self.ses_kayit = Ui_Ses_kaydi_window()
        self.ses_kayit.setupUi(self)
        
        self.ses_kayit.pushButton_SesKayd_baslat.clicked.connect(self.kaydi_baslat)
        self.ses_kayit.pushButton_SesK_Durdur.clicked.connect(self.kaydi_durdur)


        self.p = pyaudio.PyAudio()
        self.sample_rate = 44100
        self.recording = False
        self.frames = []
        self.input_device_info = self.p.get_default_input_device_info()
        self.channels = self.input_device_info['maxInputChannels']
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  input_device_index=None,
                                  stream_callback=self.audio_callback)
        

    def kaydi_baslat(self):
        self.recording = True
        self.frames = []
        self.stream.start_stream()
    
    def kaydi_durdur(self):
        self.recording = False
        self.stream.stop_stream()
        signal = np.concatenate(self.frames)
        gender = self.classify(signal)
        text = "kaydedilen sesin cinsiyeti: {}".format(gender)
        self.ses_kayit.lineEdit_Cinsiyet_text.setText(text)
        
        

        output_file = f"kaydedilen_{gender}_ses.wav"
        sf.write(output_file, signal, self.sample_rate)


    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            signal = np.frombuffer(in_data, dtype=np.float32).reshape(-1, self.channels)
            self.frames.append(signal)
            gender = self.classify(signal)
            print(f"Anlık olarak belirlenen cinsiyet: {gender}")
        return (in_data, pyaudio.paContinue)
    
    def classify(self, signal):
        if np.mean(signal[0]) > np.mean(signal[1]):
            gender = "Kadın"
        else:
            gender = "Erkek"
        return gender

    
