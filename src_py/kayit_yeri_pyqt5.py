from PyQt5.QtWidgets import *
import mysql.connector
from src_py.src_ui.kayit_yeri import Ui_girisyeri
from src_py.secim_ekran_pyqt5 import login_page
import webbrowser
import socket
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
        try:
            connection = mysql.connector.connect(
                host="awsveri.cwguyhuwi5xu.eu-north-1.rds.amazonaws.com",
                user="rise",
                password="XXXXX",
                database="kullanici_veri"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM veriler WHERE kullanici_ad = %s AND sifre = %s"
            ID = self.kayit_sayfasi.kullanici_ad_yeri.text()
            sifre = self.kayit_sayfasi.sifre_yeri.text()
            values = (ID, sifre)

            cursor.execute(query, values)
            user = cursor.fetchone()
            connection.close()
            if user:
                self.yanlis_sifre_sayac = 0
                print("tamamlandı")
                self.hide()
                self.pencere.show()

                # Kullanıcının IP adresini al
                ip_address = socket.gethostbyname(socket.gethostname())

                # IP adresini veritabanına kaydet
                connection = mysql.connector.connect(
                    host="awsveri.cwguyhuwi5xu.eu-north-1.rds.amazonaws.com",
                    user="rise",
                    password="XXXX",
                    database="kullanici_veri"
                )
                cursor = connection.cursor()
                cursor.execute('UPDATE veriler SET ip_adresi = %s WHERE kullanici_ad = %s',
                            (ip_address, ID))  
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

    def kayit_site(self):
        #self.hide()
        webbrowser.open('https://mesajlasma-41995f5c6231.herokuapp.com/', new=0)  # Kendi siteme yönlendirir.

        #web_kayit.app.run(debug=True,host="192.168.1.109")  # Flask uygulamasını başlat
        #self.show()
