from PyQt5.QtWidgets import *
import mysql.connector
from src_py.src_ui.kayit_yeri import Ui_girisyeri
from src_py.secim_ekran_pyqt5 import login_page
import time
import threading
import web_kayit
import webbrowser
import subprocess
class kayit(QMainWindow):
    def  __init__(self) -> None:
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
                host="localhost",
                user="root",
                password="Osmaniye12!",
                database="rise_together"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM kullanici_verileri WHERE kullanici_ad = %s AND kullanici_sifre = %s"
            ID = self.kayit_sayfasi.kullanici_ad_yeri.text()
            sifre = self.kayit_sayfasi.sifre_yeri.text()
            values = (ID , sifre)
            cursor.execute(query, values)
            user = cursor.fetchone()
            connection.close()
            if user:
                self.yanlis_sifre_sayac = 0
                print("tamamlandı")
                self.hide()
                self.pencere.show()  

                return True
                
            else:
                self.yanlis_sifre_sayac+=1
                print("yanlıs",self.yanlis_sifre_sayac)

                if self.yanlis_sifre_sayac == 3: # 3 kere yanlış şifre veya ID girildiğinde uygulamayı kapat
                    self.close()
                return False
        except mysql.connector.Error as err:
            print("Hata:", err)
            return False
    def kayit_site(self):
        self.hide()
        webbrowser.open('http://127.0.0.1:5000',new=0)#Kendi siteme yönlendirir.
        
        web_kayit.app.run(debug=True)  # Flask uygulamasını başlat
        self.show()







        
"""app = QApplication([])
window = kayit()
window.show()
app.exec_()"""

