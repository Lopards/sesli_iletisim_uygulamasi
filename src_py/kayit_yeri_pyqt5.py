from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,pyqtSignal
import mysql.connector
from src_py.src_ui.kayit_yeri import Ui_girisyeri
from src_py.secim_ekran_pyqt5 import login_page
import webbrowser
import atexit
import requests
import datetime
import time
import hashlib
kullanici_ad=""
 
class kayit(QMainWindow):
    kullanici_adi = pyqtSignal(str)
    def __init__(self) -> None:
        """
        Kayit sınıfının yapıcı metodudur. PyQt5 temel alınarak oluşturulan bir pencere sınıfını temsil eder.
        """
        super().__init__()

        # Kayıt sayfasının arayüzünü yükleyin
        self.kayit_sayfasi = Ui_girisyeri()
        self.kayit_sayfasi.setupUi(self)

        # Butonların tıklama olaylarını bağlayın
        self.kayit_sayfasi.pushButton.clicked.connect(self.verify_login)
        self.kayit_sayfasi.kayit_buton.clicked.connect(self.kayit_site)

        # Giriş sayfasını oluşturun
        self.pencere = login_page()

        # Yanlış şifre sayacını sıfırlayın
        self.yanlis_sifre_sayac = 0
        self.kisi_sayisi = 0
        # Veritabanı bağlantısını oluşturun
        self.connection = self.create_connection()
        atexit.register(self.cloaseEvent)

    def kullanici_ad_signal(self):
        
        return kullanici_ad
        
        

    def create_connection(self):
        """
        MySQL veritabanına bağlantı oluşturur.
        """
        return  mysql.connector.connect(
            host="rise.czfoe4l74xhi.eu-central-1.rds.amazonaws.com",
            user="admin",
            password="Osmaniye12!",
            database="rise_data"
        )

    def verify_password(self, input_password, stored_salt, stored_hashed_password):
        """
        Veritabanındaki şifreyi doğrular.

        :param input_password: Girilen şifre
        :param stored_salt: Veritabanındaki salt değeri
        :param stored_hashed_password: Veritabanındaki şifrenin hash değeri
        :return: Şifre doğru ise True, aksi takdirde False
        """
        input_salted_password = stored_salt + input_password.encode("utf-8")
        input_hashed_password = hashlib.sha256(input_salted_password).hexdigest()
        return input_hashed_password == stored_hashed_password

    def verify_login(self):
        """
        Kullanıcı girişini doğrular.
        """
        
        try:
            cursor = self.connection.cursor()

            # Kullanıcı verilerini veritabanından çek
            query = "SELECT sifre, salt  FROM veriler WHERE kullanici_ad = %s"
            ID = self.kayit_sayfasi.kullanici_ad_yeri.text()
            
            K_sifre = self.kayit_sayfasi.sifre_yeri.text()
            cursor.execute(query, (ID,))
            kullanici_verileri = cursor.fetchone()

            if kullanici_verileri:
                global kullanici_ad
                kullanici_ad = ID
                # Veritabanındaki şifreyi doğrula
                sifre = kullanici_verileri[0]
                salt_str = kullanici_verileri[1]
                salt_str = salt_str.replace(b"\x00", b"")
                salt_str_bytes = bytes(salt_str)
                is_verified = self.verify_password(K_sifre, salt_str_bytes, sifre)

                # Kullanıcının IP adresini al
                response = requests.get('https://ipinfo.io')
                ip_data = response.json()
                net_ip_adres = ip_data.get('ip')

                # Giriş tarihini kontrol et
                now = datetime.datetime.now()
                anlik_tarih = now.strftime("%Y-%m-%d %H:%M")
                ping_tarih = self.tarih_dogrulama()

                if is_verified:
                    
                    """if anlik_tarih == ping_tarih:
                        print("Hesabı başka biri kullanıyor olabilir. Lütfen 1 dakika sonra tekrar deneyiniz.")
                        BURAYI ŞU ANLIK PASİF HALE GETİRDİM TEKRAR AKTİF ETMEK İSTERSEN İF VE ELİF BLOKLARINI DÜZENLE"""
                    """if  anlik_tarih != ping_tarih:                  #elif yerine if yaptım ona göre
                        self.yanlis_sifre_sayac = 0"""


                    print("Giriş yapıldı.")
                    self.hide()
                    self.pencere.show()
                    self.ping_timer = QTimer()
                    self.ping_timer.timeout.connect(self.update_ping_date)
                    self.ping_timer.start(60000)  # 60000 milisaniye = 1 dakika

                    # Kullanıcının IP adresini ve net IP adresini veritabanına kaydet
                    cursor = self.connection.cursor()
                    cursor.execute('UPDATE veriler SET net_ip = %s, kisi_sayisi = %s WHERE kullanici_ad = %s ',
                                    (net_ip_adres, self.kisi_sayisi, ID))
                    self.connection.commit()
                    #self.connection.close()  # Bağlantıyı kapat

                    return True
                else:
                        
                        self.yanlis_sifre_sayac += 1
                        print("yanlış", self.yanlis_sifre_sayac)

                        if self.yanlis_sifre_sayac == 3:  # 3 kere yanlış şifre veya ID girildiğinde uygulamayı kapat
                            self.close()

        except mysql.connector.Error as err:
            print("Hata:", err)
            return False

    def update_ping_date(self):
        """
        Ping tarihini günceller.
        """
        try:
            cursor = self.connection.cursor()

            ID = self.kayit_sayfasi.kullanici_ad_yeri.text()

            now = datetime.datetime.now()
            today = now.strftime("%Y-%m-%d %H:%M")

            # Ping tarihini güncelle
            cursor.execute('UPDATE veriler SET ping_tarih = %s WHERE kullanici_ad = %s ',
                           (today, ID))
            self.connection.commit()
            #self.connection.close()
        except Exception as e:
            print(f"Hata: {e}")

    def tarih_dogrulama(self):
        """
        Kullanıcının son ping tarihini kontrol eder.

        :return: Son ping tarihi
        """
        # MySQL veritabanına bağlantı oluştur
        cursor = self.connection.cursor()

        # SQL sorgusu oluştur ve kullanıcı_adı parametresini kullanarak sorguyu hazırla
        sql_sorgusu = "SELECT ping_tarih FROM veriler WHERE kullanici_ad = %s"

        # Kullanıcı adı parametresini belirt
        kullanici_ad_param = self.kayit_sayfasi.kullanici_ad_yeri.text()

        # SQL sorgusunu çalıştır
        cursor = self.connection.cursor()
        cursor.execute(sql_sorgusu, (kullanici_ad_param,))

        # Sonucu al
        sonuc = cursor.fetchone()

        # Sonucu yazdır veya işle
        if sonuc:
            print(f"Kullanıcı {kullanici_ad_param}'in son ping tarihi: {sonuc[0]}")
            return sonuc[0]
        else:
            print(f"Kullanıcı {kullanici_ad_param} bulunamadı veya son ping tarihi bilgisi yok.")

        # Bağlantıyı kapat
        self.connection.close()

    
    def cloaseEvent(self): #pencere kapatıldığında bu fonksiyon devreye girer ve kullancıı sayisini azaltır.
        self.kisi_sayisi -=1
        print(self.kisi_sayisi)
        
       

    def kayit_site(self):
        """
        Web sitesine kayıt olma işlemi.
        """
        #self.hide()
        webbrowser.open('http://34.30.30.245:5000/index.html', new=0)  # Kendi siteme yönlendirir.
        #web_kayit.app.run(debug=True, host="192.168.1.109")  # Flask uygulamasını başlat
        #self.show()