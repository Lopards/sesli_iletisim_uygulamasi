from PyQt5.QtWidgets import *
from src_ui.secim_ekrani import  Secim

from istemci_pyqt5 import istemci_page
from src_ui.menu_sunucu_tarafi import MyWindow
class login_page(QMainWindow):
    def  __init__(self) -> None:
        super().__init__()
        self.login = Secim()
        self.login.setupUi(self)

        self.sunucu_taraf = MyWindow()
        self.login.SUNUCU_buton.clicked.connect(self.sunucu_app)

        self.istemci_ac = istemci_page()
        self.login.CLIENT_buton.clicked.connect(self.istemci_app) 
    def sunucu_app(self):
        self.hide()
        self.sunucu_taraf.show()
    def istemci_app(self):
        self.hide()
        self.istemci_ac.show()