from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import mysql.connector
from src_py.src_ui.kayit_yeri import Ui_girisyeri
from src_py.secim_ekran_pyqt5 import login_page
import webbrowser
import socket
import requests
import  datetime
import time  
#from src_py.server_erkek_pyqt5 import server_erkek_page
class kayit(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.kayit_sayfasi = Ui_girisyeri()
        self.kayit_sayfasi.setupUi(self)

        self.kayit_sayfasi.pushButton.clicked.connect(self.verify_login)
        self.kayit_sayfasi.kayit_buton.clicked.connect(self.kayit_site)

        self.pencere = login_page()
        self.yanlis_sifre_sayac = 0


    def verify_login(self):     
        ip_address = socket.gethostbyname(socket.gethostname())  
        try:
            connection = mysql.connector.connect(
                host="awsveri.cwguyhuwi5xu.eu-north-1.rds.amazonaws.com",
                user="rise",
                password="Osmaniye12!",
                database="kullanici_veri"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM veriler WHERE kullanici_ad = %s AND sifre = %s "
            
            ID = self.kayit_sayfasi.kullanici_ad_yeri.text()
            sifre = self.kayit_sayfasi.sifre_yeri.text()
            #durum = 'çevrimdışı'
            values = (ID, sifre)
            try:
                response = requests.get('https://ipinfo.io')
                ip_data = response.json()
                net_ip_adres=ip_data.get('ip')
               
            except Exception as e:
                print(f"Hata: {e}")
                return None


            cursor.execute(query, values)
            #cursor.execute(durum,ip_address)
            user = cursor.fetchone()
            #durum = cursor.fetchone()
            now = datetime.datetime.now()
            anlik_tarih = now.strftime("%Y-%m-%d %H:%M")
            ping_tarih = self.tarih_dogrulama()
            
            if anlik_tarih == ping_tarih:
                print("hesabı başka biri kullanıyor olabilir. Lütfen 1 dakika sonra tekrar deneyiniz")
            elif user and anlik_tarih != ping_tarih:
                self.yanlis_sifre_sayac = 0
                print("giriş yapıldı")
                self.hide()
                self.pencere.show()
                self.ping_timer = QTimer()
                self.ping_timer.timeout.connect(self.update_ping_date)
                self.ping_timer.start(2000)  # 60000 milisaniye = 1 dakika


                # Kullanıcının IP adresini al
                ip_address = socket.gethostbyname(socket.gethostname())
                
                # IP adresini veritabanına kaydet
                cursor = connection.cursor()
                cursor.execute('UPDATE veriler SET ip_adresi = %s , net_ip = %s WHERE kullanici_ad = %s ', 
                            (ip_address, net_ip_adres,  ID))  
                connection.commit()
                connection.close() #bağlantıyı kapat

                return True
            else:
                self.yanlis_sifre_sayac += 1
                print("yanlıs", self.yanlis_sifre_sayac)

                if self.yanlis_sifre_sayac == 3:  # 3 kere yanlış şifre veya ID girildiğinde uygulamayı kapat
                    self.close()
                return False
        except mysql.connector.Error as err:
            print("Hata:", err)
            return False
        
    def update_ping_date(self):
        try:
            connection = mysql.connector.connect(
                host="awsveri.cwguyhuwi5xu.eu-north-1.rds.amazonaws.com",
                user="rise",
                password="Osmaniye12!",
                database="kullanici_veri"
            )
            cursor = connection.cursor()

            ID = self.kayit_sayfasi.kullanici_ad_yeri.text()

            now = datetime.datetime.now()
            today = now.strftime("%Y-%m-%d %H:%M")

            # Ping tarihini güncelle
            cursor.execute('UPDATE veriler SET ping_tarih = %s WHERE kullanici_ad = %s ',
                           (today, ID))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"Hata: {e}")


    def  tarih_dogrulama(self):
            

            # MySQL veritabanına bağlantı oluşturun
            connection = mysql.connector.connect(
                host="awsveri.cwguyhuwi5xu.eu-north-1.rds.amazonaws.com",
                user="rise",
                password="Osmaniye12!",
                database="kullanici_veri"
            )

            # SQL sorgusu oluşturun ve kullanıcı_adı parametresini kullanarak sorguyu hazırlayın
            sql_sorgusu = "SELECT ping_tarih FROM veriler WHERE kullanici_ad = %s"

            # Kullanıcı adı parametresini belirtin
            kullanici_ad_param = self.kayit_sayfasi.kullanici_ad_yeri.text()

            # SQL sorgusunu çalıştırın
            cursor = connection.cursor()
            cursor.execute(sql_sorgusu, (kullanici_ad_param,))

            # Sonucu alın
            sonuc = cursor.fetchone()

            # Sonucu yazdırın veya işleyin
            if sonuc:
                print(f"Kullanıcı {kullanici_ad_param}'in son ping tarihi: {sonuc[0]}")
                return sonuc[0]
            else:
                print(f"Kullanıcı {kullanici_ad_param} bulunamadı veya son ping tarihi bilgisi yok.")


            # Bağlantıyı kapatın
            connection.close()

        
    def kayit_site(self):
        #self.hide()
        webbrowser.open('https://mesajlasma-41995f5c6231.herokuapp.com/', new=0)  # Kendi siteme yönlendirir.

        #web_kayit.app.run(debug=True,host="192.168.1.109")  # Flask uygulamasını başlat
        #self.show()
