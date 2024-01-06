from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from src_py.src_ui.server_man import Ui_Form
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
from flask_session import Session,sessions  
from flask import session
import socket
import pyaudio
import numpy as np
import threading
import speech_recognition as sr
import random
import socketio
import mysql.connector
from string import ascii_uppercase
from scipy import signal
import os
from cryptography.fernet import Fernet

import keyboard # tuşa basıp konuşabilmek için
sio = socketio.Client()
kullanici_ad = ""


class server_erkek_page(QWidget):
    def __init__(self) -> None:
        super().__init__()
        """self.settings = QSettings('YourCompany', 'YourApp')
        self.settingsButton = QPushButton('Ayarlar', self)
        self.settingsButton.clicked.connect(self.openSettings)"""
        self.server_erkek = Ui_Form()
        self.server_erkek.setupUi(self)
        self.background_color = "#404040"
        self.server_erkek.ip_tara.clicked.connect(self.ip_tara)
        self.server_erkek.sesli_yaz_buton.clicked.connect(self.baslat_text)
        self.server_erkek.sesli_yaz_durdur_buton.clicked.connect(
            self.stop_speech_to_text
        )
        self.server_erkek.Gonder_buton.clicked.connect(self.yazi_gonder)
        # self.server_erkek.baglanti_kur.clicked.connect(self.connect_to_server_thread)
        # self.server_erkek.settings.clicked.connect(self.settings)

        # self.server_erkek.Durdur_buton.clicked.connect(self.stop)
        self.server_erkek.baglantiyi_kes_buton.clicked.connect(self.see_members_on_room)

        # self.server_erkek.Ses_al_buton.clicked.connect(self.start_get_sound)

        # self.server_erkek.Ses_al_dur_buton.clicked.connect(self.get_sound_stop)

        self.server_erkek.hoparlo_sec_button.clicked.connect(self.play_button_clicked)
        self.server_erkek.ogrenci_hoparlor_sec.clicked.connect(self.ogr_hoparlor_sec)
        self.server_erkek.ogr_hoparlor_liste_ac.clicked.connect(self.ogr_liste_ac)
        # self.server_erkek.oda_olustur_buton.clicked.connect(self.enter_room)
        self.server_erkek.Dosya_gonder_buton.clicked.connect(self.send_file)

        self.server_erkek.Baslat_buton.setCheckable(True)
        self.server_erkek.Baslat_buton.clicked.connect(self.is_toggle_mic)
        self.server_erkek.Ses_a_devaml_buton.setCheckable(True)
        self.server_erkek.Ses_a_devaml_buton.clicked.connect(self.is_toggle_headset)
        self.server_erkek.ogr_hoparlor_liste_ac.setCheckable(True)
        self.server_erkek.hoparlor_liste_ac.setCheckable(True)
        self.server_erkek.hoparlor_liste_ac.clicked.connect(self.hoparlor_liste_ac)
 
        self.server_erkek.hoparlor_liste_ac.setCursor(
            Qt.PointingHandCursor
        )  # Bu satırı ekleyerek mouse işaretçisini değiştirebilirsiniz
        self.server_erkek.ip_tara.setCursor(Qt.PointingHandCursor)
        self.server_erkek.baglanti_kur.setCursor(Qt.PointingHandCursor)
        self.server_erkek.baglantiyi_kes_buton.setCursor(Qt.PointingHandCursor)
        self.server_erkek.Baslat_buton.setCursor(Qt.PointingHandCursor)
        self.server_erkek.Ses_a_devaml_buton.setCursor(Qt.PointingHandCursor)
        self.server_erkek.ogr_hoparlor_liste_ac.setCursor(Qt.PointingHandCursor)
        self.server_erkek.Gonder_buton.setCursor(Qt.PointingHandCursor)
        self.server_erkek.Dosya_gonder_buton.setCursor(Qt.PointingHandCursor)
        self.server_erkek.hoparlo_sec_button.setCursor(Qt.PointingHandCursor)
        self.server_erkek.ogrenci_hoparlor_sec.setCursor(Qt.PointingHandCursor)
        self.server_erkek.ogr_hoparlor_liste_ac.setCursor(Qt.PointingHandCursor)
        self.server_erkek.hoparlor_liste_ac.setCursor(Qt.PointingHandCursor)
        self.server_erkek.sesli_yaz_buton.setCursor(Qt.PointingHandCursor)
        self.server_erkek.sesli_yaz_durdur_buton.setCursor(Qt.PointingHandCursor)
        
        self.HOST = None
        self.FORMAT = pyaudio.paInt16
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 44100
        self.PITCH_SHIFT_FACTOR = 1.2

        self.metinnn = False

        self.is_running = False
        self.is_running_recv = False
        self.is_server_active = False
        self.Event = threading.Event()
        self.contunie = True
        self.flag = None
        self.metin_flag = False
        self.internet_baglantisi = False
        self.client_socket_text = None
        self.server_socket = None
        self.client_socket = None
        self.stream = None
        self.output_stream = None
        self.speaker_stream = None
        self.ip_file = "ip_addresses.txt"
        self.room_code = ""
        self.stop_event = threading.Event()
        self.sayac = 0
        self.sayac_kulaklik = 0

        self.kullanici_ad_text()
        self.hoparlor_liste()
        self.efekt_listele()
        self.ip_tara()
        self.enter_room()
        self.create_connection()

        # atexit.register(self.disconnect)
        icon_dosya = QIcon("dosya_gonder_icon.png")
        icon_ayar = QIcon("ayarlar_logo4.png")
        self.server_erkek.Dosya_gonder_buton.setIcon(icon_dosya)
        self.server_erkek.settingsButton.setIcon(icon_ayar)

    def kullanici_ad_text(
        self,
    ):  # oda kodunu db e aktarmak için bu fonksiyon kullanılacak
        from src_py.kayit_yeri_pyqt5 import (
            kayit,
        )  # kütüphane kısmında import etmedim çünkü circle hatası veriyordu.

        self.kullanici_ad = kayit()
        ID = self.kullanici_ad.kullanici_ad_signal()

        global kullanici_ad
        kullanici_ad = ID
        self.create_connection()

    def kullanici_ad_gonder(
        self,
    ):  # kullanıcı adını  istemci sayfasında kullancağım. sayfalar araası iletişim için bu fonksiyonu kullandım
        global kullanici_ad

        return kullanici_ad

    def is_toggle_mic(self):
        if self.server_erkek.Baslat_buton.isChecked():
            print("Ses gönderimi aktif")
            self.server_erkek.Baslat_buton.setText("")
            self.server_erkek.Baslat_buton.setStyleSheet(
                "QPushButton {background-color: #0d730d; border-radius:15px;color:white;}"
            )
            icon = QIcon("acikmikrofon.png")
            self.server_erkek.Baslat_buton.setIcon(icon)

            self.is_running = True
            if self.sayac == 0:
                self.sayac += 1
                print("send_audio aktif")
                self.start_communication()

        else:
            print("Ses gönderimi pasif")
            self.server_erkek.Baslat_buton.setStyleSheet(
                "QPushButton {background-color:#ff4040; border-radius:15px;color:white;}"
            )
            icon = QIcon("kapali_mic.png")
            self.server_erkek.Baslat_buton.setIcon(icon)
            self.is_running = False

    def is_toggle_headset(self):
        if self.server_erkek.Ses_a_devaml_buton.isChecked():
            print("Hoparlör aktif")
            self.Event.set()
            self.server_erkek.Ses_a_devaml_buton.setText("")
            self.server_erkek.Ses_a_devaml_buton.setStyleSheet(
                "QPushButton {background-color:#0d730d; border-radius:15px;color:white;}"
            )
            icon = QIcon("kulaklik.jpeg")
            self.server_erkek.Ses_a_devaml_buton.setIcon(icon)
            self.is_running_recv = True

        else:
            print("Hoparlör pasif")
            self.server_erkek.Ses_a_devaml_buton.setText("")
            self.Event.clear()  # eventi denicem sabahleyin unutma.
            self.server_erkek.Ses_a_devaml_buton.setStyleSheet(
                "QPushButton {background-color: #ff4040; border-radius:15px;color:white;}"
            )
            icon = QIcon("kapali_kulaklik.jpg")
            self.server_erkek.Ses_a_devaml_buton.setIcon(icon)

            self.is_running_recv = False

    def send_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Dosya Seç", "", "All Files (*)"
        )

        if not file_path:
            print("Dosya seçilmedi.")
            return

        try:
            # Dosya adını al
            file_name = os.path.basename(file_path)

            # Dosyayı oku ve Base64 ile kodla
            with open(file_path, "rb") as file:
                file_data_base64 = base64.b64encode(file.read()).decode("utf-8")

            sio.emit("file_upload", {"file_name": file_name, "file_data": file_data_base64})
            print("Dosya gönderildi")

        except Exception as e:
            print(f"Hata: {e}")

    def oda_ismi(self):  # flask için Oda kodu oluşturuyoruz
        rooms = {}
        while True:
            for _ in range(5):
                self.room_code += random.choice(ascii_uppercase)

            if self.room_code not in rooms:
                break

        self.server_erkek.oda_kod_yeri.setText(self.room_code)
        return self.room_code

    def enter_room(self):  # odaya isim ve oda kodu ile giriş yapılıyor
        name = "Doktor"
        room_code = self.oda_ismi()

        print(room_code)
        sio.on("liste", self.hoparlor_liste_al)

        sio.on("data2", self.get_sound)
        

        @sio.on("connect")
        def on_connect():
            print("Bağlandı.")
            #session["name"] = name
            #session["room"] = room_code
            sio.emit("baglan", {"name": name, "room": room_code})

        @sio.event
        def disconnect():
            print("Bağlantı kesildi.")
        
        self.create_room(name, room_code)

    def create_room(self, name, room_code):
        print("oda oluşturuldu")
        sio.connect(
            "http://192.168.1.45:5000"
        )  # Flask uygulamanızın adresine göre güncelleyin.
        sio.emit("create_room", {"name": name, "room": room_code})
        

    def efekt_listele(self):
        # Metin Gönderme sırasında seçilecek efektler listeleniyor.
        ses_efektler = ["Erkek", "Kadın", "Çocuk", "Yaşlı kadın", "Yaşlı adam"]

        for efekt in ses_efektler:
            self.server_erkek.efek_combobox.addItem(efekt)

    def hoparlor_liste(self):
        # kullanılan cihazın hoparlör listesi; arayüzde bir Listeye ekleniyor
        p = pyaudio.PyAudio()

        self.output_device_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                self.output_device_list.append(device_name)
                if len(self.output_device_list) == 6:
                    break

        model = QStandardItemModel()
        for index, device_name in enumerate(self.output_device_list):
            item = QStandardItem(device_name)
            model.appendRow(item)
            liste = f"{index + 1}. hoparlör: {device_name}"

        self.server_erkek.hoparlor_liste.setModel(model)

        #################******######################

    def ip_tara(self):
        #  kullanılan cihazın local IP adresini alıyoruz
        local_ip = socket.gethostbyname(socket.gethostname())
        self.server_erkek.ip_adres.setText(local_ip)

        #################******######################
    def see_members_on_room(self):
        room = self.room_code
        sio.emit("see_members_on_room",{"room": room})

        #################******######################

    def send_audio_e(self):
        print("ses aktarımı başladı")
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
                while keyboard.is_pressed('m'):
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)

                    converted_data = (
                        signal.resample(
                            audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR)
                        )
                        * 1.4
                    )
                    converted_data = converted_data.astype(np.int16)
                    converted_data_bytes = converted_data.tobytes()
                    audio_data = audio_data.tobytes()

                    try:
                        sio.emit("audio_data", {"audio_data": audio_data})
                        audio_data = None
                    except Exception as e:
                        print(e)
               
        except Exception as e:
            print("hata", e)
        finally:
            print("kapandı")
            stream.stop_stream()
            stream.close()
            p.terminate()

    def start_communication(self):
        print("start başlad")

        self.t = threading.Thread(target=self.send_audio_e)
        self.t.start()
        #################******######################

    def get_sound(self, data):
        try:
            if self.stream is None:
                p = pyaudio.PyAudio()
                self.stream = p.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    output=True,
                    frames_per_buffer=1024,
                )
            if data:
                audio_data = data.get("audio_data2", b"")
                # print(audio_data)
                if self.is_running_recv:
                    self.stream.write(audio_data)
            else:
                print("data yok")

        except Exception as e:
            print("Ses alma hatası:", str(e))
            """if self.stream is not None:
                        self.stream.close()
                        self.stream.stop_stream()"""

        ##### ********** ######

    def start_get_sound(self):
        self.contunie = True

        self.is_running_recv = True
        threading.Thread(target=self.get_sound).start()

        ##### ********** ######

    def hoparlor_liste_ac(self):
        if self.server_erkek.hoparlor_liste_ac.isChecked():
            self.server_erkek.hoparlor_liste_ac.setText("Hoparlör listesini kapat")
            self.server_erkek.hoparlor_liste.hide()
            self.server_erkek.hoparlo_sec_button.hide()
            self.server_erkek.hoparor_secim_frame.hide()

        else:
            self.server_erkek.hoparlor_liste_ac.setText("Hoparlör listesini aç")
            self.server_erkek.hoparlor_liste.show()
            self.server_erkek.hoparlo_sec_button.show()
            self.server_erkek.hoparor_secim_frame.show()

    def ogr_liste_ac(self):
        if self.server_erkek.ogr_hoparlor_liste_ac.isChecked():
            self.server_erkek.ogr_hoparlor_liste_ac.setText("Hoparlör listesini Kapat")
            self.server_erkek.ogrenci_hoparlor_liste.hide()
            self.server_erkek.ogrenci_hoparlor_sec.hide()

        else:
            self.server_erkek.ogr_hoparlor_liste_ac.setText("Hoparlör listesini Aç")
            self.server_erkek.ogrenci_hoparlor_liste.show()
            self.server_erkek.ogrenci_hoparlor_sec.show()

            ##### ********** ######

    def set_output_stream(self, output_device):
        """
        'play_button_clicked' fonskiyonun gönderdiği hoparlör indexini 'output_device' değişkeni ile alır
        ve pyaudio da hoparlör indexini ayarlar.

        Eğer seçilen hoparlör aktif değilse index none olarak dönecektir ve ekrana uyarı basacaktır.
        """

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
            print("Hoparlör bağlantısı yapılamadı, başka bir hoparlör seçiniz:", e)
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
                """hoparlor = self.select_output_device()
                self.set_output_stream(hoparlor)"""

        else:
            print("Hoparlör seçiniz...")

            ##### ********** ######

    def select_output_device(
        self,
    ):  # listede seçilen hoparlörün indexini al ve return et. return edilen indexi 'play_button_clicked' fonskiyonu alacak
        device_indexes = self.server_erkek.hoparlor_liste.selectedIndexes()
        if device_indexes:
            selected_row = device_indexes[0].row()
            output_device_index = selected_row
            # print(output_device_index)
            return output_device_index
        else:
            # Eğer herhangi bir öğe seçilmemişse veya listede yanlış değer seçilmişse , None döndür
            return None

    def play_button_clicked(
        self,
    ):  # Hoparlör listesinde seçilen hoparlörü 'set_output_stream' fonskyinonuna gönder.
        output_device = self.select_output_device()
        self.set_output_stream(output_device)
        self.stop_event.clear()
        # self.play_server_output(data)

    def connect(self):  # internet bağlantısını kontrol eder ve ekrana uyarı basar.
        while True:
            try:
                socket.gethostbyname("www.google.com")
                if not self.internet_baglantisi:
                    print("İnternet bağlantısı aktif.")
                    self.internet_baglantisi = True
                return True
            except socket.gaierror:
                if self.internet_baglantisi:
                    print("İnternet bağlantısı yok! Uyarı: Bağlantı kopmuş olabilir.")
                    self.internet_baglantisi = False
                return False

            #################******######################

    def sesi_anlik_yaziya_cevir(self):
        while self.flag:
            r = sr.Recognizer()

            with sr.Microphone() as source:
                print("Dinleme başladı. Konuşun...")

                while self.flag:
                    audio = r.listen(source)

                    try:
                        text = r.recognize_google(audio, language="tr-TR")
                        if text:
                            self.server_erkek.metin_yeri.insertPlainText(
                                text + ". "
                            )  # mikrosondan gelen cümleyi metin alanına aktar ve sonuna '.' koy
                    except sr.UnknownValueError:
                        print("Ses anlaşılamadı.")
                    except sr.RequestError as e:
                        print("İstek başarısız oldu; {0}".format(e))

        print("mikrofon kapandı.")

        #################******######################

    def baslat_text(self):
        # sesi_anlik_yaziya_cevir fonks. başlat
        self.flag = True
        threading.Thread(target=self.sesi_anlik_yaziya_cevir).start()

        #################******######################

    def stop_speech_to_text(self):
        # sesi_anlik_yaziya_cevir fonks. durdur
        self.flag = False
        #################******######################

    def yazi_gonder(self):
        room = self.room_code

        name = "Doktor"

        try:
            message = self.server_erkek.metin_yeri.toPlainText()
            secili_efekt = (
                self.server_erkek.efek_combobox.currentIndex()
            )  # comboboxda ki efekti al
            efekt = int(secili_efekt)

            # Anahtar oluştur
            key = self.generate_key()  # text için key oluştur

            encrypted_message = self.encrypt_message(message, key)  # Mesajı şifrele

            # flaskta ki message olayına şifreli mesajı- room-efekt ve keyi sözcük içinde emitle
            sio.emit(
                "message",
                {
                    "data": encrypted_message.decode(),
                    "room": room,
                    "name": name,
                    "efekt": efekt,
                    "key": key,
                },
            )
        except KeyboardInterrupt:
            pass

            # sio.wait()

            # sio.disconnect()

            #################******######################

    def yazi_gonder_t(self):
        t1 = threading.Thread(target=self.yazi_gonder)
        t1.start()

    def generate_key(self):
        return Fernet.generate_key()  # key oluştur

    def encrypt_message(self, message, key):  # keyi ve mesajı al
        cipher_suite = Fernet(key)  # şifreli paketi oluştur
        encrypted_message = cipher_suite.encrypt(
            message.encode()
        )  # şifrelenmiş mesajı oluştur ve return et
        return encrypted_message

    def get_background_color(self):
        return self.background_color

    def create_connection(self):
        """
        MySQL veritabanına bağlantı oluşturur.
        """
        global kullanici_ad
        print(kullanici_ad)
        connection = mysql.connector.connect(
            host="rise.czfoe4l74xhi.eu-central-1.rds.amazonaws.com",
            user="admin",
            password="Osmaniye12!",
            database="rise_data",
        )
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE veriler SET oda_kodu =%s WHERE kullanici_ad = %s ",
            (self.room_code, kullanici_ad),
        )
        connection.commit()
        connection.close()

 
    def hoparlor_liste_al(self, Liste):
        # öğrenci tarafından gelen hoparlor listesini al ve arayüzdeki listeye aktar
        hoparlor_liste = Liste["list"]
        print("liste geldi")
        model = QStandardItemModel()
        for device_name in hoparlor_liste:
            item = QStandardItem(device_name)
            model.appendRow(item)
        self.server_erkek.ogrenci_hoparlor_liste.setModel(model)

    def ogr_hoparlor_sec(self):
        # Seç butonu ile ögrenci hoparlörünü seç ve seçilen indexi istemciye yolla
        selected = self.server_erkek.ogrenci_hoparlor_liste.selectedIndexes()
        selected_row = selected[0].row()  # İndexin ilk elemanını al
        print(selected_row)
        sio.emit("output_device_index", {"index": selected_row}) # index sözcüğü ile gönder



