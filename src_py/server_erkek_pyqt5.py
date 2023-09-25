from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from src_py.src_ui.server_man import Ui_Form
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import atexit #program aniden kapansa bile 69. satır sayesinde sql database durum = çıkıldı yapılıyor.
import mysql.connector#sql bağlantısı
import socket
import pyaudio
import numpy as np
import threading
import speech_recognition as sr
import time
import pickle
from scipy import signal
class server_erkek_page(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.server_erkek = Ui_Form()
        self.server_erkek.setupUi(self)

        self.server_erkek.ip_tara.clicked.connect(self.ip_tara)
        self.server_erkek.sesli_yaz_buton.clicked.connect(self.baslat_text)
        self.server_erkek.sesli_yaz_durdur_buton.clicked.connect(self.stop_speech_to_text)
        self.server_erkek.Gonder_buton.clicked.connect(self.yazi_gonder)
        self.server_erkek.baglanti_kur.clicked.connect(self.connect_to_server_thread)

        self.server_erkek.Baslat_buton.clicked.connect(self.start)
        self.server_erkek.Durdur_buton.clicked.connect(self.stop)
        self.server_erkek.baglantiyi_kes_buton.clicked.connect(self.disconnect)

        #self.server_erkek.Ses_al_buton.clicked.connect(self.start_get_sound)
        self.server_erkek.Ses_a_devaml_buton.clicked.connect(self.get_sound_contunie)
        self.server_erkek.Ses_al_dur_buton.clicked.connect(self.get_sound_stop)

        self.server_erkek.hoparlo_sec_button.clicked.connect(self.play_button_clicked)
        self.server_erkek.ogrenci_hoparlor_sec.clicked.connect(self.ogr_hoparlor_sec)
        self.HOST = None
        self.PORT = 12345
        self.PORT_TEXT =12346
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 22050
        self.PITCH_SHIFT_FACTOR = 1.2
        
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
       
        self.hoparlor_liste()
        self.efekt_listele()
        self.ip_tara()
        atexit.register(self.disconnect)
         
    
    def efekt_listele(self):
        #Metin Gönderme sırasında seçilecek efektler listeleniyor.
        ses_efektler = ["Erkek", "Kadın", "Çocuk","Yaşlı kadın","Yaşlı adam"]

        for efekt in ses_efektler:
            self.server_erkek.efek_combobox.addItem(efekt)


    def hoparlor_liste(self):
        #kullanılan cihazın hoparlör listesi; arayüzde bir Listeye ekleniyor 
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
        for index,device_name in enumerate(self.output_device_list):
            item = QStandardItem(device_name)
            model.appendRow(item)
            liste = f"{index+1}. hoparlör: {device_name}"

            

        self.server_erkek.hoparlor_lis.setModel(model)
        
        #################******######################
    def ip_tara(self):

        #  kullanılan cihazın local IP adresini alıyoruz
        local_ip = socket.gethostbyname(socket.gethostname())
        self.server_erkek.ip_adres.setText(local_ip)

        

        #################******######################         

    def hoparlor_liste_al(self):
        #öğrenci tarafından gelen hoparlor listesini al ve arayüzdeki listeye aktar
        hoparlor_liste_str = self.client_socket.recv(4016)
        hoparlor_liste = pickle.loads(hoparlor_liste_str)

        model = QStandardItemModel()
        for device_name in hoparlor_liste:
            item = QStandardItem(device_name)
            model.appendRow(item)

        self.server_erkek.ogrenci_hoparlor_liste.setModel(model)
        #################******######################
               
    def ogr_hoparlor_sec(self):
        #Seç butonu ile ögrenci hoparlörünü seç ve seçilen indexi istemciye yolla 
        selected_efect = self.server_erkek.ogrenci_hoparlor_liste.selectedIndexes()
        selected_row = selected_efect[0].row()  # İndexin ilk elemanını al
        selected_efect_bytes = selected_row.to_bytes(10, byteorder="big")  # İndexi 10 byte olarak gönder
        self.client_socket.send(selected_efect_bytes)


        #################******######################

    def connect_to_server(self):
        #bağlantılara açık olmaya yarıyor
        selected_ip = self.server_erkek.ip_adres.text() 
        self.HOST = selected_ip
        

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(1)
        print(f"* Bağlantı için {self.HOST}:{self.PORT} dinleniyor...")

        self.client_socket, address = self.server_socket.accept()#gelen isteği kabul et
        print(f"* {address} adresinden bir bağlantı alındı.")
        
        excepted_mesaj = "Beklenen_Mesaj"
        received_mesaj = self.client_socket.recv(1024).decode()
        if received_mesaj == excepted_mesaj: #mesajlar aynı ise iletişime geçilecek

            print("ses göndermek için ilk iönce öğrenci tarafın hoparlörünü seçiniz...")
            #burada ara satırlara time.sleep(1) koydum çünkü tek thread ile yaptığımdan aynı anda yapamıyordu, başka thread koymak istemedim.
            time.sleep(1)
            self.hoparlor_liste_al()
            self.yazi_gonder_t()

            time.sleep(1)
            #self.start()

            time.sleep(1)
            self.start_get_sound()
            
            time.sleep(1)
            self.get_sound_contunie()
            
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
        else:
             print("Dikkat, cihazınız tarandı!")
             self.connect_to_server()

        #self.client_socket.close()
        #self.server_socket.close()
        

    def connect_to_server_thread(self):
         #connect_to_server'i thread ile başlat
         threading.Thread(target=self.connect_to_server).start()

            #################******######################
    def disconnect(self):
        """
        Ses Gönderim ve ses alma işlemlerini durdur
        ve Bağlantıları kapat
        """

        self.is_running = False  
        self.is_running_recv = False
        self.contunie = False
        
        if self.client_socket is not None:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
                time.sleep(1)
                print("sunucu kapandi")
            except (OSError, AttributeError):
                pass
           
        
        if self.server_socket is not None:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
                time.sleep(1)
                print("sunucu kapandı")
            except (OSError, AttributeError):
                pass
            
            #################******######################
    

    def send_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
        Esik_deger = 80 # mikrofon hassasiyetini belirleyecek değer
        
        while self.is_running:
            self.connect()#internet bağlantısı kontrolü yapılıyor, internet yoksa uyarı veriyor, tekrar bağlanırsada uyarı veriyor.
            
            
            data = stream.read(self.CHUNK) # mikrofondan gelen verileri oku
            audio_data = np.frombuffer(data, dtype=np.int16) #okunan verileri numpy dizisine donuştur
            if np.abs(audio_data).mean() > Esik_deger: # mikrofona gelen ses verilerin MUTLAK değerinin ortalamasını alarak ses şiddetini buluyoruz. ortalama, eşik değerinden yüksekse ses iletim devam ediyor.
                mikrofon = True
                
            else:
                mikrofon  = False
            
            try:
                    if self.is_running and mikrofon:
                    
                        converted_data = signal.resample(audio_data, int(len(audio_data) * self.PITCH_SHIFT_FACTOR)) #PITCH_SHIFT_FACTOR ile sesin örnekleme sayısını değiştir
                        converted_data = converted_data.astype(np.int16)#yeniden işlenen ses verisini int16 tam sayısına dönüştür
                        converted_data_bytes = converted_data.tobytes()#ses verisini baytlara donuştur
                        self.client_socket.sendall(converted_data_bytes) #istemciye yolla

                    if not self.is_running:
                            return
          
            
            except Exception as e:  #Herhangi bir hata olursa programı tekrar açmak zorunda kalmadan bağlantıları tekrar aç
                    if self.client_socket is not None and self.contunie == True:
                        print("bir hata oldu : ",e)
                        print("yeniden bağlanılmaya çalışılıyor...")
                        self.client_socket.close()
                        self.client_socket, address = self.server_socket.accept()
                        print(f"* {address} adresinden yeni bir bağlantı alındı.")
                        self.yazi_gonder_t()
        

         #işlem sonunda tüm bağlantıları durdur ve kapat
        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        p.terminate()

            #################******######################
    
    def get_sound_fonc(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.CHANNELS,
            rate=self.RATE,
            output=True
        )
        
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
                
                        self.play_server_output(data) #ses verisini play_server_output fonksiyonuna gönder. bu fonksiyon sayesinde seçilen hoparlöre ses gönderilecek

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

    def select_output_device(self):     #listede seçilen hoparlörün indexini al ve return et. return edilen indexi 'play_button_clicked' fonskiyonu alacak
        device_indexes = self.server_erkek.hoparlor_lis.selectedIndexes()
        if device_indexes:
            selected_row = device_indexes[0].row()
            output_device_index = selected_row
           # print(output_device_index)
            return output_device_index
        else:
            # Eğer herhangi bir öğe seçilmemişse veya listede yanlış değer seçilmişse , None döndür
            return None


    def play_button_clicked(self):  #Hoparlör listesinde seçilen hoparlörü 'set_output_stream' fonskyinonuna gönder.
        
        output_device = self.select_output_device()
        self.set_output_stream(output_device)
        self.stop_event.clear()
        #self.play_server_output(data)



    def connect(self): #internet bağlantısını kontrol eder ve ekrana uyarı basar.
        

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
                                
                                self.server_erkek.metin_yeri.insertPlainText(text + ". ") #mikrosondan gelen cümleyi metin alanına aktar ve sonuna '.' koy
                    except sr.UnknownValueError:
                            print("Ses anlaşılamadı.")
                    except sr.RequestError as e:
                            print("İstek başarısız oldu; {0}".format(e))

        print("mikrofon kapandı.")

            #################******######################
    def baslat_text(self):
        #sesi_anlik_yaziya_cevir fonks. başlat
            self.flag = True
            threading.Thread(target=self.sesi_anlik_yaziya_cevir).start()

            #################******######################        

    def stop_speech_to_text(self):
        #sesi_anlik_yaziya_cevir fonks. durdur
        self.flag = False
            #################******######################   
    def yazi_gonder(self):
            """
            Metin göndermek için ayrı bir socket bağlantısı kuruyorum.
            Bunun sebebi ses verileriyle metin verilerinin birbirleriyle karışması ve istenmedik sorunlara yol açmasıydı.
            """       
            try:
                if not self.metin_flag:
                    server_socket_text = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket_text.bind((self.HOST, self.PORT_TEXT))
                    server_socket_text.listen(1)           
                    print(f"* Metin için {self.HOST}:{self.PORT_TEXT} dinleniyor...")

                    self.client_socket_text, address = server_socket_text.accept()
                    print(f"* Metin için {address} bağlanıldı.")

                    self.metin_flag = True  # Bayrağı True olarak ayarla, böylece tekrardan bağlantı kurmuyor

                metin = self.server_erkek.metin_yeri.toPlainText().strip() #metin alanındaki yazıları alıyoruz
                
                

                if metin:
                    # Metin verisini ikinci soket üzerinden gönder
                    self.client_socket_text.send(bytes(metin, "utf-8")) #metni utf-8 koduyla gönderiyoruz
                    self.server_erkek.metin_yeri.clear()

                    selected_efect = self.server_erkek.efek_combobox.currentIndex()
                    selected_efect_bytes = selected_efect.to_bytes(10, byteorder="big")  # seçilen efekt indexini 10 byte olarak gönder
                    self.client_socket_text.send(selected_efect_bytes)
                    print("Metin gönderildi:", metin)
            except Exception as e:
                print("metin gönderme işlemi duraklatıldı...", e)
                # Bağlantı hatası oluştuğunda, tekrar bağlantı kurmak için bayrağı False yap
                self.metin_flag = False
                # Socketi kapat ve yeniden bağlantıyı kurmak için çağrı yap
                if self.client_socket_text:
                    self.client_socket_text.close()
        

            #################******######################
    def yazi_gonder_t(self):

        t1 = threading.Thread(target=self.yazi_gonder)
        t1.start()

"""app = QApplication([])
window = server_erkek_page()
window.show()
app.exec_()"""
