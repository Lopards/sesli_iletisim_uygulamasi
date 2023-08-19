from PyQt5.QtWidgets import *
from src_ui.istemci import Ui_Dialog
from PyQt5.QtWidgets import QListWidgetItem
import threading
import pyaudio
import numpy as np
import socket
import nmap
import time
import pickle
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from src_metin.metin_oku import *

class istemci_page(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.istemci = Ui_Dialog()
        self.istemci.setupUi(self)

        self.istemci.ip_tara_buton.clicked.connect(self.scan_ip)
        self.istemci.baglan_buton.clicked.connect(self.connect_to_server)

        self.istemci.ses_gonder_buton.clicked.connect(self.start_communication)
        self.istemci.Ses_gonder_dur.clicked.connect(self.stop_communication)
        #self.istemci.Ses_al_buton.clicked.connect(self.get_sound)
        self.istemci.ses_al_devam.clicked.connect(self.get_sound_continue)
        self.istemci.ses_al_duraklat.clicked.connect(self.get_sound_stop)
        self.istemci.baglantiyi_kes_buton.clicked.connect(self.disconnect)
        #self.istemci.metin_okuma_buton.clicked.connect(self.metni_oku)


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
        self.istemci.ip_listesi.itemDoubleClicked.connect(self.item_double_clicked)
        
        self.ip_listesini_comboboxa_ekle()
        #self.scan_ip()


    def receive_text(self):
        metin_flag = False
        try:
            if not metin_flag:
                server_socket_text = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket_text.connect((self.HOST, self.PORT_TEXT))
            # self.server_socket,adress = se
                print(f"Metin için Bağlantı sağlandı: {self.HOST}")
                metin_flag = True
        except:
            print("metin alma işlemi duraksadı.")

        while True:
            try:
                data = server_socket_text.recv(1024)
                

                metin = data.decode("utf-8")
                
                self.istemci.metin_yeri.insertPlainText(metin+". ")
                alinan_index_bytes = server_socket_text.recv(10)  # 10 byte olarak gelen veriyi al
                alinan_index = int.from_bytes(alinan_index_bytes, byteorder="big")
                #self.alinan_index_bytes = server_socket_text.recv(10)

                #metin = self.istemci.metin_yeri.toPlainText()
                print(alinan_index)
                
                # alınan_index değeri; sunucu tarafından gelen efekt seçimidir. 0 = erkek, 1 = kadın .....
                if alinan_index == 0:
                    
                    read_man(metin)
                    
                    
                    #self.istemci.metin_yeri.clear()    

                elif alinan_index ==1:
                    read_text__woman_thread(metin)
                    
                elif alinan_index == 2:
                    read_children(metin)
                    
                elif alinan_index == 3:
                    read_old_woman(metin)

                elif alinan_index == 4:
                    read_old_man(metin)
                
                
                
                


            except ConnectionResetError:
                if not metin_flag:
                    server_socket_text = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket_text.connect((self.HOST, self.PORT_TEXT))
                # self.server_socket,adress = se
                    print(f"Metin için Bağlantı sağlandı: {self.HOST}")
                    metin_flag = True
                break
        server_socket_text.close()

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
                    self.connect_to_server()
           

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

    def receive_audio(self):
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
                    self.connect_to_server()
                    
                    data = self.server_socket.recv(self.CHUNK)

                    if not data:
                        break

                    if self.Event.is_set() and self.contunie:
                        stream.write(data)
                    

        stream.stop_stream()
        stream.close()
        self.server_socket.close()
        p.terminate()
        #şu anda yeniden bağlanmada sorun var hop. listesi gönderilmeli


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

    def hoparlor_liste(self):
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
            item = QStandardItem(device_name)  # Yalnızca bir metin (string) verisi ekle
            model.appendRow(item)

        hoparlor_liste_str = pickle.dumps(self.output_device_list)
        self.server_socket.send(hoparlor_liste_str)



        


        
        
    def connect_to_server(self):
        nm = nmap.PortScanner()
        nm.scan('192.168.1.0/24', arguments='-p {}'.format(self.PORT))
        hosts = nm.all_hosts()
        
        server_ip = None  # Sadece socket ile sunucu açan bilgisayarın IP adresi

        for host in hosts:
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.settimeout(3)
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
                print("olmadi")
                pass

        # IP adresi bulunduysa, listeye ekleyin
        

    def disconnect(self):
        self.is_running = False  # Gönderim ve ses alma işlemlerini durdur
        self.is_running_recv = False
        self.contunie = False

        if self.server_socket is not None:
            try:

                self.server_socket.shutdown(socket.SHUT_RDWR)   
                self.server_socket.close()
            except (OSError,AttributeError):
                print("gg")
                pass
       

    def scan_ip(self):
        
        nm = nmap.PortScanner()
        nm.scan('192.168.1.0/24', arguments='-p {}'.format(self.PORT))
        hosts = nm.all_hosts()

        server_ip = None  # Sadece socket ile sunucu açan bilgisayarın IP adresi

        for host in hosts:
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.settimeout(1)
                server_socket.connect((host, self.PORT))
                server_socket.close()
                server_ip = host
                print(f"Sadece socket ile sunucu açan bilgisayarın IP Adresi: {server_ip}")
                break
            except (ConnectionRefusedError, socket.timeout):
                pass

        # IP adresi bulunduysa, listeye ekleyin
        if server_ip:
            itemtext = f"{server_ip}"
            item = QListWidgetItem(itemtext)
            self.istemci.ip_listesi.addItem(item)

        #self.listbox.insert(tk.END,ip_address+"     "+str(mac_address))
    def item_double_clicked(self, item):
        # Çift tıklanan seçeneğin metnini al
        selected_text = item.text()
        ip_adres = selected_text.split()[0]
        # Metni ip_combobox'a ekle
        self.istemci.ip_combobox.addItem(ip_adres)


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


    def save_ip_address(self, ip_address):
            with open(self.ip_file, "a") as f:
                f.write(ip_address + "\n")
       

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