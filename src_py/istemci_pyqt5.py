from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from src_py.src_ui.istemci import Ui_Form
from PyQt5.QtWidgets import QListWidgetItem
import threading
import pyaudio
import numpy as np

import time

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from src_py.src_metin.metin_oku import *
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor, QBrush
import requests
from bs4 import BeautifulSoup
import socketio
from cryptography.fernet import Fernet
import base64
import os

sio = socketio.Client()


class istemci_page(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.istemci = Ui_Form()
        self.istemci.setupUi(self)
        self.background_color = "#404040"
        """self.istemci.ip_tara_buton.clicked.connect(self.scan_ip)
        self.istemci.otomatik_baglan_buton.clicked.connect(
            self.connect_to_server_Automatic
        )
        self.istemci.manuel_baglan.clicked.connect(self.connect_to_server_Manuel)"""

        # self.istemci.ses_al_devam.clicked.connect(self.get_sound_continue)

        self.istemci.baglantiyi_kes_buton.clicked.connect(self.disconnect)

        self.istemci.odaya_gir_buton.clicked.connect(self.enter_room)

        self.istemci.ses_gonder_buton.setCheckable(True)
        self.istemci.ses_gonder_buton.clicked.connect(self.start_communication)

        self.istemci.ses_al_devam.setCheckable(True)
        self.istemci.ses_al_devam.clicked.connect(self.is_toggle_headset)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

        self.HOST = None  # Sunucu IP adresi
        self.PORT = 12345  # Sunucu port numarası
        self.PORT_TEXT = 12346
        self.contunie = True
        self.is_running = False
        self.is_running_recv = True
        self.is_reading = False
        self.Thread = None

        self.Event = threading.Event()
        self.stop_event = threading.Event()
        self.output_stream = None
        self.server_socket = None
        self.stream = None
        self.p = pyaudio.PyAudio()
        
        self.sio = socketio.Client()

        self.ip_file = "ip_addresses.txt"  # IP adreslerini saklayan dosya adı
        self.istemci.ip_listesi.itemDoubleClicked.connect(self.item_double_clicked)

        self.ip_listesini_comboboxa_ekle()
        # self.receive_file()
        self.istemci.ip_tara_buton.setCursor(
            Qt.PointingHandCursor
        )  # Bu satırı ekleyerek mouse işaretçisini değiştir
        self.istemci.manuel_baglan.setCursor(Qt.PointingHandCursor)
        self.istemci.otomatik_baglan_buton.setCursor(Qt.PointingHandCursor)
        self.istemci.odaya_gir_buton.setCursor(Qt.PointingHandCursor)
        self.istemci.ses_al_devam.setCursor(Qt.PointingHandCursor)
        self.istemci.ses_gonder_buton.setCursor(Qt.PointingHandCursor)
        self.istemci.baglantiyi_kes_buton.setCursor(Qt.PointingHandCursor)

        # self.scan_ip()

    def is_toggle_microfon(self):  # ses gönderimini kapatıp açmak için bir fonksiyon
        if self.istemci.ses_gonder_buton.isChecked():
            print("Ses gönderimi aktif")
            self.istemci.ses_gonder_buton.setText("Mikrofon açık")
            self.istemci.ses_gonder_buton.setStyleSheet(
                "QPushButton {background-color:lightgreen}"
            )
            if not self.is_running:
                self.is_running = True
                threading.Thread(target=self.send_audio).start()
        else:
            print("Ses gönderimi pasif")
            self.istemci.ses_gonder_buton.setText("Mikrofon kapalı")
            self.istemci.ses_gonder_buton.setStyleSheet(
                "QPushButton {background-color:lightcoral}"
            )
            if self.is_running:
                self.is_running = False

    def is_toggle_headset(self):  # ses alımını kapatıp açmak için bir fonksiyon
        if self.istemci.ses_al_devam.isChecked():
            print("Kulaklık aktif")
            self.istemci.ses_al_devam.setText("Kulaklık açık")
            self.istemci.ses_al_devam.setStyleSheet(
                "QPushButton {background-color:lightgreen}"
            )

            self.is_running_recv = True
        else:
            print("Kulaklık pasif")
            self.istemci.ses_al_devam.setText("Kulaklık kapalı")
            self.istemci.ses_al_devam.setStyleSheet(
                "QPushButton {background-color:lightcoral}"
            )
            self.is_running_recv = False

    @sio.on("file_uploaded")
    def receive_file2(data):
        try:
            file_name = data["filename"]  # "file_uploaded" olayında "filename" olarak emit ediliyor
            file_data_base64 = data["file_data"]

            # Base64 veriyi çöz
            #file_data = base64.b64decode(file_data_base64)
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
            file_path = os.path.join("downloads", file_name)

            with open(file_path, "wb") as file:
                file.write(file_data_base64)

            print("Dosya alındı:", file_name)
        except Exception as e:
            print(f"Hata dosya alınırken: {e}")

    
    def decrypt_message(self, encrypted_message, key):  #gelen şifreli metni ve keyi alıyoruz.   
        cipher_suite = Fernet(base64.urlsafe_b64encode(key).decode("utf-8"))
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode() #şifreleri çözüp normal asıl metnimize ulaşıyoruz
        return decrypted_message

    def receive_text(self):
        @sio.event
        def connect():
            print("Connected to server")

        @sio.on("message") #flask projesindeki message olayına 'on' ile bağlanıyoruz. bu şekilde mesaj gönderildiğinde handle_message aktif olacak
        def handle_message(message):
            print(message)
            print("s")
            if "message" in message:
                text = message.get("message", "")  # Şifreli mesaj içeriğini al
                efekt = message.get("efekt", "")  # Efekti al
                key = message.get("key", "")  # Anahtarı al

                if text == "has entered the room":
                    pass
                else:
                    # Mesajı çöz
                    print(key)
                    key = base64.urlsafe_b64decode(key.decode("utf-8"))  # Anahtarı çöz
                    decrypted_message = self.decrypt_message(text, key)
                    
                    self.istemci.metin_yeri.insertPlainText(
                        f"Mesaj: {decrypted_message}\n"
                    )  # Çözülmüş mesajı pyqt5 alanına ekle ve efekte göre okut
                    if efekt == 0:
                        read_man(decrypted_message)
                    elif efekt == 1:
                        read_text__woman_thread(decrypted_message)
                    elif efekt == 2:
                        read_children(decrypted_message)
                    elif efekt == 3:
                        read_old_woman(decrypted_message)
                    elif efekt == 4:
                        read_old_man(decrypted_message)
            else:
                print(message)
                pass

    def enter_room(self):  # flask ile kurulan odaya giriş yapılıyor. Ses ve metin alışverişi başlatılıyor
        room = self.istemci.Oda_kodu_yeri.text()
        name = "öğrenci"

        # self.get_sound_f()
        self.receive_text()
        self.start_communication()
        sio.on("data1", self.get_sound)
        sio.connect("http://192.168.1.56:5000", auth={"name": name, "room": room})

    def receive_text_thread(self):
        ti1 = threading.Thread(target=self.receive_text)
        ti1.start()

    def send_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.CHANNELS,
            rate=44100,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        try:
            while True:
                if self.is_running != True:

                    data = stream.read(self.CHUNK)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    
                    audio_data = audio_data.tobytes()

                    sio.emit(
                        "audio_data2", {"audio_data2": audio_data}
                    )  # Bytlara dönüştürülen ses verilerini 'audio_data' sözcüğü ile emitle emitle
        except Exception as e:
            print("hata")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def start_communication(self):
        threading.Thread(target=self.send_audio).start()

    

    # @sio.on('audio_data')
    def get_sound(self):
            try:
                # Stream'i burada aç
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    output=True,
                )
                print(stream)

                @sio.on("data1")
                def ses_al(data):
                    try:

                        while self.is_running_recv and stream is not None:
                            audio_data = data.get("audio_data", b"")
                            print(audio_data)
                            stream.write(audio_data)
                        else:
                            print("------")
                    except Exception as e:
                        print("Hata:", str(e))
            except Exception as e:
                print("hata",e)
        



    def get_sound_f(self):
        self.is_running_recv = True
        threading.Thread(target=self.get_sound).start()
        # self.get_sound_button.config(state="disabled")

    

    
    def item_double_clicked(self, item):
        # Çift tıklanan seçeneğin metnini al
        selected_text = item.text()
        ip_adres = selected_text.split()[0]
        # Metni ip_combobox'a ekle
        self.istemci.ip_combobox.addItem(ip_adres)
        self.save_ip_address(ip_adres)

    def ip_listesini_comboboxa_ekle(self):
        ip_addresses = []
        try:
            with open(self.ip_file, "r") as f:
                for line in f:
                    ip_addresses.append(line.strip())
        except FileNotFoundError:
            pass

        # Alınan IP adreslerini combobox'a ekle
        for ip_address in ip_addresses:
            self.istemci.ip_combobox.addItem(ip_address)
            # self.save_ip_address(ip_address)

    def save_ip_address(self, ip_address):
        with open(self.ip_file, "r") as f:
            ip_addresses = [line.strip() for line in f]

        if ip_address not in ip_addresses:
            ip_addresses.insert(0, ip_address)  # Yeni IP adresini en üstte ekleyin

            with open(
                self.ip_file, "w"
            ) as f:  # Dosyanın içeriğini yeniden yazmak için "w" modunu kullanın
                for ip in ip_addresses:
                    f.write(ip + "\n")



    def set_output_stream(self, output_device):
        p = pyaudio.PyAudio()
        try:
            self.output_stream = p.open(
                output=True,
                format=pyaudio.paInt16,
                channels=self.CHANNELS,
                rate=self.RATE,
                frames_per_buffer=self.CHUNK,
                output_device_index=output_device,
            )
        except OSError as e:
            print("Hoparlör bağlantısı yapılamadı:", e)
            self.output_stream = None
            ##### ********** ######

    def play_server_output(self, data):
        if self.output_stream is not None:
            try:
                self.output_stream.write(data)
            except OSError as e:
                print("Hoparlör bağlantısı koparıldı:", e)
                self.output_stream.close()
                self.output_stream.stop_stream()
                self.output_stream = None

        else:
            print("Hoparlör seçiniz...")

            ##### ********** ######

    def select_output_device(self):
        index_bytes = self.server_socket.recv(
            10
        )  # İhtiyaca göre byte sayısını ayarlayın
        index = int.from_bytes(index_bytes, byteorder="big")
        print(index)
        device_indexes = index
        print(device_indexes)
        if device_indexes is not None:
            return device_indexes
        else:
            # Eğer herhangi bir öğe seçilmemişse, None döndür
            return None

    def play_button_clicked(self):
        output_device = self.select_output_device()
        print(output_device)
        if output_device is not None:
            print("Output Device:", output_device)
            self.set_output_stream(output_device)
            self.stop_event.clear()
        else:
            print("Hoparlör seçilmedi. Devam edemiyoruz.")

        # self.play_server_output(data)

    def get_background_color(self):
        return self.background_color

"""app = QApplication([])
window = istemci_page()
window.show()
app.exec_()"""
