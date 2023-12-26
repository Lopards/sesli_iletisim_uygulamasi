from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from src_py.src_ui.istemci import Ui_Form
from PyQt5.QtWidgets import QListWidgetItem
import threading
import pyaudio
import numpy as np
import mysql.connector
import time

from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
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

        self.istemci.baglantiyi_kes_buton.clicked.connect(self.send_output_device_list)

        self.istemci.odaya_gir_buton.clicked.connect(self.oda_kodu_ID)

        self.istemci.ses_gonder_buton.setCheckable(True)
        self.istemci.ses_gonder_buton.clicked.connect(self.is_toggle_mic)

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
        self.is_running_recv = False
        self.is_reading = False
        self.Thread = None

        self.Event = threading.Event()
        self.stop_event = threading.Event()
        self.output_stream = None
        self.server_socket = None
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.sio = socketio.Client()
        self.sayac_kulaklik = 0
        self.sayac = 0
        self.device_indexes= None
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
        self.istemci.ses_al_devam.setDisabled(True)
        # self.oda_kodu_ID()
        # self.scan_ip()

    def is_toggle_mic(self):
        if self.istemci.ses_gonder_buton.isChecked() and not self.is_running:
            print("Ses gönderimi aktif")
            self.istemci.ses_gonder_buton.setText("")
            self.istemci.ses_gonder_buton.setStyleSheet(
                "QPushButton {background-color: #0d730d; border-radius:15px;color:white;}"
            )
            icon = QIcon("acikmikrofon.png")
            self.istemci.ses_gonder_buton.setIcon(icon)
            self.is_running = True
            if self.sayac == 0:
                self.sayac += 1
                print("send_audio aktif")
                self.start_communication()



        else:
            print("Ses gönderimi pasif")
            self.istemci.ses_gonder_buton.setStyleSheet(
                "QPushButton {background-color:#ff4040; border-radius:15px;color:white;}"
            )
            icon = QIcon("kapali_mic.png")
            self.istemci.ses_gonder_buton.setIcon(icon)
            self.is_running = False

    def is_toggle_headset(self):
        if self.istemci.ses_al_devam.isChecked():
            print("Hoparlör aktif")
            self.istemci.ses_al_devam.setText("")
            self.istemci.ses_al_devam.setStyleSheet(
                "QPushButton {background-color: #0d730d; border-radius:15px;color:white;}"
            )
            icon = QIcon("kulaklik.jpeg")
            self.istemci.ses_al_devam.setIcon(icon)

            print(self.sayac_kulaklik)
            self.is_running_recv = True

        else:
            print("Hoparlör pasif")
            self.istemci.ses_al_devam.setStyleSheet(
                "QPushButton {background-color:#ff4040; border-radius:15px;color:white;}"
            )
            icon = QIcon("kapali_kulaklik.jpg")
            self.istemci.ses_al_devam.setIcon(icon)
            self.is_running_recv = False

    @sio.on("file_uploaded")
    def receive_file2(data):
        try:
            file_name = data["filename"]  # "file_uploaded" olayında "filename" olarak emit ediliyor
            file_data_base64 = data["file_data"]

            # Base64 veriyi çöz
            # file_data = base64.b64decode(file_data_base64)
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
            file_path = os.path.join("downloads", file_name)

            with open(file_path, "wb") as file:
                file.write(file_data_base64)

            print("Dosya alındı:", file_name)
        except Exception as e:
            print(f"Hata dosya alınırken: {e}")

    def decrypt_message(
            self, encrypted_message, key
    ):  # gelen şifreli metni ve keyi alıyoruz.
        cipher_suite = Fernet(base64.urlsafe_b64encode(key).decode("utf-8"))
        decrypted_message = cipher_suite.decrypt(
            encrypted_message
        ).decode()  # şifreleri çözüp normal asıl metnimize ulaşıyoruz
        return decrypted_message

    def receive_text(self):
        @sio.event
        def connect():
            print("Connected to server")

        @sio.on(
            "message"
        )  # flask projesindeki message olayına 'on' ile bağlanıyoruz. bu şekilde mesaj gönderildiğinde handle_message aktif olacak
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

    def enter_room(
            self,
    ):  # flask ile kurulan odaya giriş yapılıyor. Ses ve metin alışverişi başlatılıyor
        room = self.istemci.Oda_kodu_yeri.text()
        name = "öğrenci"

        self.receive_text()

        #self.send_output_device_list()
        sio.on("index",self.select_output_device)

        sio.on("data1", self.get_sound)
        sio.connect("http://192.168.1.75:5000", auth={"name": name, "room": room})


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

            while self.is_running == True:
                data = stream.read(self.CHUNK)
                audio_data = np.frombuffer(data, dtype=np.int16)

                audio_data = audio_data.tobytes()

                sio.emit("audio_data2", {
                    "audio_data2": audio_data})  # Bytlara dönüştürülen ses verilerini 'audio_data' sözcüğü ile emitle emitle
        except Exception as e:
            print("hata", e)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def start_communication(self):
        threading.Thread(target=self.send_audio).start()

    def get_sound(self, data):
        while not self.output_stream:
            self.play_button_clicked()

        try:

            if data:
                audio_data = data.get("audio_data", b"")
                # print(audio_data)
                if self.is_running_recv:
                    self.play_server_output(audio_data)
                    #self.stream.write(audio_data)

        except Exception as e:
            print("Ses alma hatası:", str(e))

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

    def select_output_device(self,index):
        row = index['index']
        
        self.device_indexes = row
        print(self.device_indexes)
        if self.device_indexes is not None:
            return self.device_indexes
        else:
            # Eğer herhangi bir öğe seçilmemişse, None döndür
            return None

    def play_button_clicked(self):
        
        print(self.device_indexes)
        try:
            if self.device_indexes is not None:
                print("Output Device:", self.device_indexes)
                self.set_output_stream(self.device_indexes)
                self.istemci.ses_al_devam.setDisabled(False)
                #self.stop_event.clear()
            else:
                print("Hoparlör seçilmedi. Devam edemiyoruz.")
                return
        except Exception as e:
            print("hoparlör seçiminde hata:",e)
        # self.play_server_output(data)

    def get_background_color(self):
        return self.background_color

    def oda_kodu_ID(self):
        from src_py.kayit_yeri_pyqt5 import kayit  # kütüphane kısmında import etmedim çünkü circle hatası veriyordu.
        self.kullanici_ad = kayit()
        ID = self.kullanici_ad.kullanici_ad_signal()
        print(ID)

        """
        MySQL veritabanına bağlantı oluşturur.
        """

        connection = mysql.connector.connect(
            host="rise.czfoe4l74xhi.eu-central-1.rds.amazonaws.com",
            user="admin",
            password="Osmaniye12!",
            database="rise_data"
        )
        cursor = connection.cursor()
        query = "SELECT oda_kodu FROM veriler WHERE kullanici_ad = %s"
        cursor.execute(query, (ID,))
        kullanici_verileri = cursor.fetchone()

        connection.commit()
        connection.close()
        self.istemci.Oda_kodu_yeri.setText(kullanici_verileri[0])
        self.enter_room()

    def send_output_device_list(self):  # cihazın hoparlör listesini server bilgisayara pickle ile yolla
        p = pyaudio.PyAudio()

        output_device_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                output_device_list.append(device_name)
                if len(output_device_list) == 8:
                    break
        print("yolladım")
        sio.emit("output_device_list",  {"list": output_device_list})


    


"""app = QApplication([])
window = istemci_page()
window.show()
app.exec_()"""
