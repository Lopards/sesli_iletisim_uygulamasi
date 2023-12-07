from PyQt5.QtWidgets import *
from src_py.src_ui.istemci import Ui_Form
from PyQt5.QtWidgets import QListWidgetItem
import threading
import pyaudio
import numpy as np
import socket
import nmap
import time
import pickle
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from src_py.src_metin.metin_oku import *
from PyQt5.QtWidgets import QListWidgetItem 
from PyQt5.QtGui import QColor, QBrush
import requests
from bs4 import BeautifulSoup
import socketio
from cryptography.fernet import Fernet  
import base64
sio = socketio.Client()

class istemci_page(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.istemci = Ui_Form()
        self.istemci.setupUi(self)

        self.istemci.ip_tara_buton.clicked.connect(self.scan_ip)
        self.istemci.otomatik_baglan_buton.clicked.connect(self.connect_to_server_Automatic)
        self.istemci.manuel_baglan.clicked.connect(self.connect_to_server_Manuel)

        #self.istemci.ses_gonder_buton.clicked.connect(self.start_communication)
        #self.istemci.Ses_gonder_dur.clicked.connect(self.stop_communication)
        #self.istemci.Ses_al_buton.clicked.connect(self.get_sound)
        self.istemci.ses_al_devam.clicked.connect(self.get_sound_continue)
        #self.istemci.ses_al_duraklat.clicked.connect(self.get_sound_stop)
        self.istemci.baglantiyi_kes_buton.clicked.connect(self.disconnect)
        #self.istemci.metin_okuma_buton.clicked.connect(self.metni_oku)
        self.istemci.odaya_gir_buton.clicked.connect(self.receive_text_thread)
        self.istemci.odaya_gir_buton.clicked.connect(self.receive_file2_t)
        
        self.istemci.ses_gonder_buton.setCheckable(True)
        self.istemci.ses_gonder_buton.clicked.connect(self.is_toggle_microfon)

        self.istemci.ses_al_devam.setCheckable(True)
        self.istemci.ses_al_devam.clicked.connect(self.is_toggle_headset)
        self.CHUNK = 512 
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 22050

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


        self.ip_file = "ip_addresses.txt"  # IP adreslerini saklayan dosya adı
        #self.istemci.ip_listesi.itemDoubleClicked.connect(self.item_double_clicked)
        
        self.ip_listesini_comboboxa_ekle()
        #self.scan_ip()
    def is_toggle_microfon(self):# ses gönderimini kapatıp açmak için bir fonksiyon
        if self.istemci.ses_gonder_buton.isChecked():
            print("Ses gönderimi aktif")
            self.istemci.ses_gonder_buton.setText("Mikrofon açık")
            self.istemci.ses_gonder_buton.setStyleSheet("QPushButton {background-color:lightgreen}")
            if not self.is_running:
                self.is_running = True
                threading.Thread(target=self.send_audio).start()
        else:   
            print("Ses gönderimi pasif")
            self.istemci.ses_gonder_buton.setText("Mikrofon kapalı")
            self.istemci.ses_gonder_buton.setStyleSheet("QPushButton {background-color:lightcoral}")
            if self.is_running:
                self.is_running = False

    def is_toggle_headset(self):# ses alımını kapatıp açmak için bir fonksiyon
        if self.istemci.ses_al_devam.isChecked():
            print("Kulaklık aktif")
            self.istemci.ses_al_devam.setText("Kulaklık açık")
            self.istemci.ses_al_devam.setStyleSheet("QPushButton {background-color:lightgreen}")
            self.Event.set()
        else:   
            print("Kulaklık pasif")
            self.istemci.ses_al_devam.setText("Kulaklık kapalı")
            self.istemci.ses_al_devam.setStyleSheet("QPushButton {background-color:lightcoral}")
            self.Event.clear()

    def handle_client(self,client_socket):
        try:
            # Sunucudan dosya boyutunu al
            file_size = int(client_socket.recv(1024).decode())

            # Dosya adını al
            file_name = client_socket.recv(1024).decode()

            # Dosyayı al
            file_data = client_socket.recv(file_size)

            # Dosyayı kaydet
            with open(file_name, 'wb') as file:
                file.write(file_data)

            print(f"{file_name} başarıyla kaydedildi.")
        except Exception as e:
            print("Hata:", e)
        finally:
            client_socket.close()

    def receive_file2(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 12345
        server_socket.bind((host, port))
        server_socket.listen(5)

        print(f"Sunucu {host}:{port} portunda dinliyor...")

        while True:
            # İstemci bağlantısını kabul et
            client_socket, client_address = server_socket.accept()
            print(f"{client_address} bağlandı.")

            # İstemciye hizmet veren bir thread başlat
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()
    def receive_file2_t(self):
        threading.Thread(target=self.receive_file2).start()


    def decrypt_message(self, encrypted_message, key):
        cipher_suite = Fernet(base64.urlsafe_b64encode(key).decode('utf-8'))
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message
        


    def receive_text(self):
        @sio.event
        def connect():
            print('Connected to server')

        @sio.on('message')
        def handle_message(message):
            if 'message' in message:
                text = message.get('message', '')  # Şifreli mesaj içeriğini al
                efekt = message.get('efekt', '')  # Efekti al
                key = message.get('key', '')  # Anahtarı al
                print(key,text)
                if text == "has entered the room":
                    pass
                else:
                    # Mesajı çöz
                   
                    #key = base64.urlsafe_b64encode(key).decode('utf-8')
                    key = base64.urlsafe_b64decode(key.decode('utf-8'))  # Anahtarı çöz
                    #key = base64.urlsafe_b64decode(key)  # Anahtarı çöz
                    decrypted_message = self.decrypt_message(text, key)
                    print(decrypted_message, "zaaaaa")
                    self.istemci.metin_yeri.insertPlainText(f'Mesaj: {decrypted_message}\n')  # Çözülmüş mesajı pyqt5 alanına ekle
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
                print('Received invalid message:', message)


        room = self.istemci.Oda_kodu_yeri.text() 
        name = "öğrenci"

        sio.connect('http://35.202.241.22:5000', auth={"name": name, "room": room})

        try:
            while True:
                pass  # Sürekli olarak mesajları dinlemek için döngüyü sürdürün
        except KeyboardInterrupt:
            pass  # Ctrl+C ile çıkış yapılabilir

        sio.disconnect()
        
    def receive_text_thread(self):
        ti1 = threading.Thread(target=self.receive_text)
        ti1.start()
       

    def send_audio(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)

        min_esik_deger = 100
        max_esik_deger = 850

        while self.is_running:
            
            data = stream.read(self.CHUNK)
            audio_data = np.frombuffer(data, np.int16)
            

            try:
                sound_vol = np.abs(audio_data).mean()
                if min_esik_deger < sound_vol < max_esik_deger: # mikrofona gelen ses verilerin MUTLAK değerinin ortalamasını alarak ses şiddetini buluyoruz. ortalama, eşik değerinden yüksekse ses iletim devam ediyor.
                    mikrofon = True
                
                else:
                    mikrofon  = False
                    """
                    gelen ses verisi ortalaması max esik değerin üstünde ise sesin seviyesi azzaltılıyor
                    eğer ses verisi ortalaması min esik değerin altında ise sesin seviyesi arttırılıyor.
                    """
                    if sound_vol > max_esik_deger:
                        audio_data = (audio_data // 3).astype(np.int16)
                        mikrofon = True
                    elif sound_vol < min_esik_deger:
                        audio_data = (audio_data * 5).astype(np.int16)
                        mikrofon = True

                if self.is_running and mikrofon:
                    
                    self.server_socket.sendall(audio_data)
                if not self.is_running:
                    return
            except Exception as e:
                if self.server_socket is not None and self.contunie ==True:

                    print("Beklenmedik bir hata oluştu... Lütfen bekleyiniz: ", e)
                    print("Yeniden bağlanılmaya çalışılıyor.")
                    self.connect_to_server_Automatic()
           

        stream.stop_stream()
        stream.close()
        p.terminate()

    def start_communication(self):
        if not self.is_running:
            self.is_running = True
            threading.Thread(target=self.send_audio).start()
    
    def stop_communication(self):
        if self.is_running:
            self.is_running = False

    def get_sound(self, data):
        try:
            self.p = pyaudio.PyAudio()
            audio_data = data["data"]
            print(audio_data)
           
            self.stream = self.p.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    output=True)

            self.stream.write(audio_data)
        except Exception as e:
            print("Error:", str(e))

    def ses_al(self):
        sio.on('get_audio', self.get_sound)
        sio.emit('get_audio', callback=lambda data: self.get_sound(data)) # flasktan ses almak için denedim şu anda ses verilerini hoparlörde çalamıyorum

    """def receive_audio(self):
        #hoparlor=self.select_output_device()
        
        while not self.output_stream:
            self.play_button_clicked()
            
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True)
        
        
        while self.is_running_recv:
            
            try:
                
                data = self.server_socket.recv(self.CHUNK)
                
                if not data:
                    break

                if self.Event.is_set() and self.contunie:
                    #stream.write(data)
                    
                    self.play_server_output(data)
            except Exception as e:
                if self.server_socket is not None and self.contunie:
                    print("Bağlantı sıfırlandı... Yeniden bağlanılıyor.\n", e)
                    self.connect_to_server_Automatic()
                    
                    data = self.server_socket.recv(self.CHUNK)

                    if not data:
                        break

                    if self.Event.is_set() and self.contunie:
                        stream.write(data)
                    

        stream.stop_stream()
        stream.close()
        self.server_socket.close()
        p.terminate()
        #şu anda yeniden bağlanmada sorun var hop. listesi gönderilmeli"""


    def get_sound(self):
        self.is_running_recv = True
        threading.Thread(target=self.receive_audio).start()
        #self.get_sound_button.config(state="disabled")
    def get_sound_stop(self):
        self.Event.clear()


    def get_sound_continue(self):
        self.Event.set()

        
    def server_hoparlor(self):
        hoparlor_listesi_str = self.server_socket.recv(4096)
        hoparlor_listesi = pickle.loads(hoparlor_listesi_str)
        for index,hoparlor in enumerate(hoparlor_listesi):
            listele=f"{index+1}.Hoparlor: {hoparlor}"
            print(listele)

    def hoparlor_liste(self): # cihazın hoparlör listesini server bilgisayara pickle ile yolla 
        p = pyaudio.PyAudio()

        self.output_device_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                device_name = device_info["name"]
                self.output_device_list.append(device_name)
                if len(self.output_device_list) == 8:
                    break

        model = QStandardItemModel()
        for index, device_name in enumerate(self.output_device_list):
            item = QStandardItem(device_name)  # Yalnızca bir metin (string) verisi ekle
            model.appendRow(item)

        hoparlor_liste_str = pickle.dumps(self.output_device_list)
        self.server_socket.send(hoparlor_liste_str)



        


        
        
    def connect_to_server_Automatic(self):  # Bu fonksiyon aktif olduğunda socket ile açılan servera otomatik olarak bağlanır. 
        ip_address = socket.gethostbyname(socket.gethostname())

        # IP adresinin ilk üç bölümünü alarak IP aralığı oluştur
        ip_range = '.'.join(ip_address.split('.')[:3]) + '.0/24' # bu güncelleme ile ip adres kodu değişse de ip taraması yapılabiecek
        nm = nmap.PortScanner()
        nm.scan(ip_range, arguments='-p {}'.format(self.PORT))
        hosts = nm.all_hosts()
        
        server_ip = None  # Sadece socket ile sunucu açan bilgisayarın IP adresi

        for host in hosts:
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.server_socket.settimeout(1)
                
                server_ip = host
                print(f"Sadece socket ile sunucu açan bilgisayarın IP Adresi: {server_ip}")

                """if server_ip:
                    itemtext = f"{server_ip}"
                    item = QListWidgetItem(itemtext)
                    self.istemci.ip_listesi.addItem(item)"""
        
        
                #combobox'daki seçilen ip adresini Host'a ata
                #selected_ip = self.istemci.ip_combobox.currentText()
                self.HOST = server_ip
                
                #self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.connect((self.HOST, self.PORT))
                print(f"Bağlantı sağlandı: {self.HOST}")
                time.sleep(1)
                #self.server_hoparlor()
                self.hoparlor_liste()
            # Hoparlör listesini terminalde göster
                
                time.sleep(1)
                self.receive_text_thread()
                
                time.sleep(1)
                self.get_sound()
                
                time.sleep(1)
                self.get_sound_continue()

                self.start_communication()
                time.sleep(1)

                
                
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




                break
            except (ConnectionRefusedError, socket.timeout):
                print("Sanırım Bu değil")
                pass

        # IP adresi bulunduysa, listeye ekleyin
        

    def disconnect(self):
        """
        ses gönderim ve ses alım işlemlerini durdur.
        Bağlantıları kapat"""
        self.is_running = False  
        self.is_running_recv = False
        self.contunie = False

        if self.server_socket is not None:
            try:

                self.server_socket.shutdown(socket.SHUT_RDWR)   
                self.server_socket.close()
            except (OSError,AttributeError):
                print("gg")
                pass
       

    def scan_ip(self):  # çevredeki diğer cihazların ip numaralarını listeler
        
        import ping3
        ip_address = socket.gethostbyname(socket.gethostname())
        ip_range = '.'.join(ip_address.split('.')[:3]) + '.0/24'
        nm = nmap.PortScanner()
        nm.scan(ip_range, arguments='-sn')
        hosts = nm.all_hosts()
        print("Ağdaki tüm cihazların IP ve MAC adresleri:")
        
        expected_message = "Beklenen6_Mesaj"  # Eşleşmesi beklenen mesaj
        
        for host in hosts:
            if 'mac' in nm[host]['addresses']:
                ip_address = nm[host]['addresses']['ipv4']
                mac_address = nm[host]['addresses']['mac']
                
                # Ping gönder
                response_time = ping3.ping(ip_address)
                
                # Socket ile bağlantı denemesi yap (istek göndermeden)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)  # Bağlantı zaman aşımı süresi 1 saniye
                
                result = s.connect_ex((ip_address, 12345))  # Örnek olarak 80 portuna bağlantı denemesi yapılıyor
                
                s.close()
                
                if response_time is not None:
                    ping_status = "Açık"
                else:
                    ping_status = "Kapalı"
                    
                if result == 0:
                    socket_status = "Açık"
                    
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1)  # Bağlantı zaman aşımı süresi 1 saniye
                        s.connect((ip_address, 12345))  # Örnek olarak 12345 portuna bağlanıyoruz
                        s.send(expected_message.encode())  # Beklenen mesajı gönder
                        s.close()
                        
                        # Taradığınız IP adresini yeşil olarak işaretleyin
                        for i in range(self.istemci.ip_listesi.count()):
                            item = self.istemci.ip_listesi.item(i)
                            if item is not None:
                                ip_from_list = item.text().split()[0]
                                if ip_from_list == ip_address:
                                    brush_background = QBrush(QColor("green"))
                                    brush_foreground = QBrush(QColor("white"))
                                    item.setBackground(brush_background)
                                    item.setForeground(brush_foreground)
                        
                    except (socket.timeout, ConnectionRefusedError):
                        s.close()
                else:
                    socket_status = "Kapalı"
                    
                item_text = f"{ip_address}    {mac_address}    Ping: {ping_status}    Socket: {socket_status}"
                item = QListWidgetItem(item_text)
                self.istemci.ip_listesi.addItem(item)
                for i in range(self.istemci.ip_listesi.count()):
                    if socket_status=="Açık":
                       brush_background = QBrush(QColor("green"))
                       brush_foreground = QBrush(QColor("white"))
                       item.setBackground(brush_background)
                       item.setForeground(brush_foreground)     

                



    def connect_to_server_Manuel(self):
        # combobox da seçilen ip numarasına kullanıcı isterse "manuel bağlan" tuşu iele bağlanılır...
        #combobox'daki seçilen ip adresini Host'a ata
        #manuel bağlanma başlatıldı.
        try:
            selected_ip = self.istemci.ip_combobox.currentText()
            self.HOST = selected_ip
            print("{} - bağlanılmaya çalışıyor".format(self.HOST))
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.HOST, self.PORT))
            print(f"Bağlantı sağlandı: {self.HOST}")
            
            time.sleep(1)
            #self.server_hoparlor()
            self.hoparlor_liste()
        # Hoparlör listesini terminalde göster

            time.sleep(1)
            self.receive_text_thread()

            time.sleep(1)
            self.get_sound()


            time.sleep(1)
            self.get_sound_continue()
            self.start_communication()
            time.sleep(1)
            
            
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
        except socket.error as e:
            pass



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
            #self.save_ip_address(ip_address)


    def save_ip_address(self, ip_address):
        with open(self.ip_file, "r") as f:
            ip_addresses = [line.strip() for line in f]

        if ip_address not in ip_addresses:
            ip_addresses.insert(0, ip_address)  # Yeni IP adresini en üstte ekleyin

            with open(self.ip_file, "w") as f:  # Dosyanın içeriğini yeniden yazmak için "w" modunu kullanın
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
        index_bytes = self.server_socket.recv(10)  # İhtiyaca göre byte sayısını ayarlayın
        index = int.from_bytes(index_bytes,byteorder="big")
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


        
        #self.play_server_output(data)
        
"""app = QApplication([])
window = istemci_page()
window.show()
app.exec_()"""
