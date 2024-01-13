from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from src_py.src_ui.server_kadin import Ui_Form

from PyQt5.QtGui import QStandardItem, QStandardItemModel

import socket
import pyaudio
import numpy as np
import threading
import speech_recognition as sr
import time
from scipy import signal
class server_kadin_page(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.server_kadin = Ui_Form()
        self.server_kadin.setupUi(self)

        self.server_kadin.ip_tara.clicked.connect(self.ip_tara)
        self.server_kadin.sesli_yaz_buton.clicked.connect(self.baslat_text)
        self.server_kadin.baglanti_kur.clicked.connect(self.connect_to_server_thread)

        self.server_kadin.Baslat_buton.clicked.connect(self.start)
        self.server_kadin.Durdur_buton.clicked.connect(self.stop)

        self.server_kadin.Ses_al_buton.clicked.connect(self.start_get_sound)
        self.server_kadin.Ses_a_devaml_buton.clicked.connect(self.get_sound_contunie)
        self.server_kadin.Ses_al_dur_buton.clicked.connect(self.get_sound_stop)

        self.server_kadin.hoparlo_sec_button.clicked.connect(self.play_button_clicked)
        
        self.server_kadin.baglantiyi_kes_buton.clicked.connect(self.disconnect)

        
        
        self.HOST = None
        self.PORT = 12345
        self.PORT_TEXT =12346
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 22050
        self.PITCH_SHIFT_FACTOR = 0.8
        
        self.metinnn= False
        

        

        self.is_running = False
        self.is_running_recv = True
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
        
        self.stop_event = threading.Event()

        
        
        self.liste_olustur()


    
         
    def liste_olustur(self):
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
        for device_name in self.output_device_list:
            item = QStandardItem(device_name)
            model.appendRow(item)
            

        self.server_kadin.listView.setModel(model)
        
        
    def ip_tara(self):
        #  local IP adresini alıyoruz
        local_ip = socket.gethostbyname(socket.gethostname())
        self.server_kadin.ip_adres.setText(local_ip)
        

    def connect_to_server_thread(self):
         threading.Thread(target=self.connect_to_server).start()

    def connect_to_server(self):
        selected_ip = self.server_kadin.ip_adres.text()
        self.HOST = selected_ip
        print(self.HOST)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(1)
        print(f"* Bağlantı için {self.HOST}:{self.PORT} dinleniyor...")

        self.client_socket, address = self.server_socket.accept()
        print(f"* {address} adresinden bir bağlantı alındı.")
        #self.yazi_gonder_t()
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        speaker_stream = p.open(format=pyaudio.paInt16,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    output=True)
        

        stream.stop_stream()
        stream.close()
        speaker_stream.stop_stream()
        speaker_stream.close()
        p.terminate()

        #self.client_socket.close()
        #self.server_socket.close()


    def disconnect(self):
            
        self.is_running = False  # Gönderim ve ses alma işlemlerini durdur
        self.is_running_recv = False
        self.contunie = False
        
        if self.client_socket is not None:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except (OSError, AttributeError):
                pass
           
        
        if self.server_socket is not None:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
            except (OSError, AttributeError):
                pass
            
        
        


        

  
        
    
    """def get_saved_ip_addresses(self):
        ip_addresses = []
        try:
            with open(self.ip_file, "r") as f:
                for line in f:
                    ip_addresses.append(line.strip())
        except FileNotFoundError:
            pass
        return ip_addresses

    def save_ip_address(self, ip_address):
        with open(self.ip_file, "a") as f:
            f.write(ip_address + "\n")"""
    

    def send_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
        Esik_deger = 30
        
        while self.is_running:
            self.connect()
            
            
            data = stream.read(self.CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            if np.abs(audio_data).mean() > Esik_deger: # mikrofona gelen ses verilerin MUTLAK değerinin ortalamasını alarak ses şiddetini buluyoruz. ortalama, eşik değerinden yüksekse ses iletim devam ediyor.
                mikrofon = True
                
            else:
                mikrofon  = False
                
            
            
            try:
                    if self.is_running and mikrofon:
                    
                        converted_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR)) * 1.4
                        converted_data = converted_data.astype(np.int16)
                        converted_data_bytes = converted_data.tobytes()
                        self.client_socket.sendall(converted_data_bytes)

                    if not self.is_running:
                            return
          
            
            except Exception as e:
                    if self.client_socket is not None and self.contunie == True:
                        print("bir hata oldu : ",e)
                        print("yeniden bağlanılmaya çalışılıyor...")
                        self.client_socket.close()
                        self.client_socket, address = self.server_socket.accept()
                        print(f"* {address} adresinden yeni bir bağlantı alındı.")
        

         
                    


        
        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        p.terminate()


    
    def get_sound_fonc(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.CHANNELS,
            rate=self.RATE,
            output=True
        )
        Esik_deger = 100
        while self.is_running_recv:
            # İnternet bağlantısını kontrol et
            check_net = self.connect()
            if not check_net:
                # Eğer bağlantı yoksa uygun uyarıyı ver ve bir süre bekle
                print("İnternet bağlantısı yok! Uyarı: Bağlantı kopmuş olabilir.")
                time.sleep(3)
                continue

            try:
                data = self.client_socket.recv(self.CHUNK)
                if not data:
                    break
                if self.Event.is_set() and self.contunie:
                    
                        self.play_server_output(data)

                else:
                    print("Ses al devam tuşuna bas")
            except Exception as e:
                if self.client_socket is not None and self.contunie:
                    print("Beklenmeyen bir hata oluştu:", e)
                    print("Yeni bir bağlantı bekleniyor...")
                    self.client_socket.close()
                    self.client_socket, address = self.server_socket.accept()
                    print(f"* {address} adresinden yeni bir bağlantı alındı.")
            

        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        p.terminate()
        
        
                
    

                            ##### ********** ######        
    def start_get_sound(self):
        self.contunie = True
        
        self.is_running_recv = True
        threading.Thread(target=self.get_sound_fonc).start()
        

                            ##### ********** ######

    def get_sound_stop(self):
        self.Event.clear()
        #self.is_running_recv = False
        
                            ##### ********** ######
    def get_sound_contunie(self):
        self.Event.set()
        
        
                            ##### ********** ######
    def start(self):
        if  self.is_running !=True:
            self.is_running = True
            threading.Thread(target=self.send_audio).start()
                            ##### ********** ######
    def stop(self):
        
            self.is_running = False
            


                             ##### ********** ###### 
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
                """hoparlor = self.select_output_device()
                self.set_output_stream(hoparlor)"""
                
                
        else:
            print("Hoparlör seçiniz...")
            
                        ##### ********** ######
    def select_output_device(self):
        device_indexes = self.server_kadin.listView.selectedIndexes()
        if device_indexes:
            selected_row = device_indexes[0].row()
            output_device_index = selected_row
            print(output_device_index)
            return output_device_index
        else:
            # Eğer herhangi bir öğe seçilmemişse, None döndür
            return None


    def play_button_clicked(self):
        output_device = self.select_output_device()
        self.stop_event.clear()
        self.set_output_stream(output_device)
        #self.play_server_output(data)



    def connect(self):
        

        while True:
            try:
                # www.google.com adresine bağlanmayı dene (80 ve 443 portları genellikle açıktır)
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
                                
                                self.server_kadin.textEdit.insertPlainText(text+ '. ')
                    except sr.UnknownValueError:
                            print("Ses anlaşılamadı.")
                    except sr.RequestError as e:
                            print("İstek başarısız oldu; {0}".format(e))

        print("mikrofon kapandı.")

    def baslat_text(self):
        
            self.flag = True
            threading.Thread(target=self.sesi_anlik_yaziya_cevir).start()
        

    def stop_speech_to_text(self):
        #sei yazıya dökme durdur
        self.flag = False
    
    def yazi_gonder(self):
        
            try:
                if not self.metin_flag:
                    server_socket_text = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket_text.bind((self.HOST, self.PORT_TEXT))
                    server_socket_text.listen(1)           
                    print(f"* Metin için {self.HOST}:{self.PORT_TEXT} dinleniyor...")

                    self.client_socket_text, address = server_socket_text.accept()
                    print(f"* Metin için {address} bağlanıldı.")

                    self.metin_flag = True  # Bayrağı True olarak ayarla, böylece tekrardan bağlantı kurmuyor

                metin = self.server_kadin.textEdit.toPlainText().strip()

                if metin:
                    # Metin verisini ikinci soket üzerinden gönder
                    self.client_socket_text.send(bytes(metin, "utf-8"))
                    self.server_kadin.textEdit.clear()
                    print("Metin gönderildi:", metin)
            except Exception as e:
                print("metin gönderme işlemi duraklatıldı...", e)
                # Bağlantı hatası oluştuğunda, tekrar bağlantı kurmak için bayrağı False yap
                self.metin_flag = False
                # Socketi kapat ve yeniden bağlantıyı kurmak için çağrı yap
                if self.client_socket_text:
                    self.client_socket_text.close()
        

        


    def yazi_gonder_t(self):
        """if not self.metin_flag:
            self.metin_flag = True"""
        t1 = threading.Thread(target=self.yazi_gonder)
        t1.start()

    
"""app = QApplication([])
window = server_kadin_page()
window.show()
app.exec_()"""