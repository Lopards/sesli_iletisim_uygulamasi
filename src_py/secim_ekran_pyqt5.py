from PyQt5.QtWidgets import *
from src_py.src_ui.secim_ekrani import  Secim

from src_py.istemci_pyqt5 import istemci_page
from src_py.src_ui.menu_sunucu_tarafi import MyWindow
import webbrowser
"""
Doktor butonu sunucu tarafı,
Öğrenci butonu ise istemci tarafı çalıştırır.
"""
class login_page(QMainWindow):
    def  __init__(self) -> None:
        super().__init__()
        self.login = Secim()
        self.login.setupUi(self)

        self.sunucu_taraf = MyWindow()
        self.login.SUNUCU_buton.clicked.connect(self.sunucu_app)

        self.istemci_ac = istemci_page()
        self.login.CLIENT_buton.clicked.connect(self.istemci_app) 
        self.login.link.clicked.connect(self.link)
    def sunucu_app(self):
        self.hide()
        self.sunucu_taraf.show()
    def istemci_app(self):
        self.hide()
        self.istemci_ac.show()
    def link(self):
        QLabel
        webbrowser.open('https://sites.google.com/view/emirhanerdem/ana-sayfa', new=0)#Kendi siteme yönlendirir.