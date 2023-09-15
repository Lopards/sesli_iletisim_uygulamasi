from PyQt5.QtWidgets import QApplication
from src_py.kayit_yeri_pyqt5 import kayit
#seçim ekranını çalıştırır.
app = QApplication([])
pencere = kayit()
pencere.show()
app.exec_() 