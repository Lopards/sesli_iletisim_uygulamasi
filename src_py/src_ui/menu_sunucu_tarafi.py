import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QVBoxLayout, QWidget
from src_py.server_erkek_pyqt5 import server_erkek_page
from src_py.server_kadin_pyqt5 import server_kadin_page
from src_py.sunucu_pyqt5 import Sunucu_page
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.server = server_erkek_page()
       

    def initUI(self):
        self.setWindowTitle("Doktor - Menü")
        self.setGeometry(100, 100, 400, 300)

        # Menü oluşturma
        menubar = self.menuBar()
        menu = menubar.addMenu("Seçenekler")

        #Burada menu seçeneklerini oluşturuyoruz
        ses_islemleri = QAction("ses işlemleri", self)
        ses_islemleri.triggered.connect(self.ses_islemleri)
        menu.addAction(ses_islemleri)

        interkom_e = QAction("interkom (erkek)", self)
        interkom_e.triggered.connect(self.interkom_e)
        menu.addAction(interkom_e)

        interkom_k = QAction("interkom (kadın)", self)
        interkom_k.triggered.connect(self.interkom_k)
        menu.addAction(interkom_k)

        


        # İçerik göstermek için bir widget oluştur
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        
        sunucu = Sunucu_page()
        self.layout.addWidget(sunucu)

    def interkom_e(self):
        # Mevcut pencerenin içeriğini temizle
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
    # server_erkek_page sınıfından bir nesne oluştur
        server_erkek = server_erkek_page()
        
        # Oluşturulan nesneyi mevcut pencerenin içeriği olarak ayarla
        self.layout.addWidget(server_erkek)

    def interkom_k(self):
        # Mevcut pencerenin içeriğini temizle
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    # server_erkek_page sınıfından bir nesne oluştur
        server_kadin = server_kadin_page()
        
        # Oluşturulan nesneyi mevcut pencerenin içeriği olarak ayarla
        self.layout.addWidget(server_kadin)

    def ses_islemleri(self):
        # Mevcut pencerenin içeriğini temizle
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    # server_erkek_page sınıfından bir nesne oluştur
        sunucu = Sunucu_page()
        
        # Oluşturulan nesneyi mevcut pencerenin içeriği olarak ayarla
        self.layout.addWidget(sunucu)
"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
"""