import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Butonları oluştur
        button1 = QPushButton('Buton 1', self)
        button2 = QPushButton('Buton 2', self)

        # Düzeni oluştur
        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)

        # Ana pencereye düzeni ekle
        self.setLayout(vbox)

        # Pencereyi boyutlandırma ve gösterme
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('PyQt5 Otomatik Boyutlandırma')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()
    sys.exit(app.exec_())
