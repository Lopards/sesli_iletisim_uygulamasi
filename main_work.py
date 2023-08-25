from PyQt5.QtWidgets import QApplication
from  src_py.secim_ekran_pyqt5 import login_page
#seçim ekranını çalıştırır.
app = QApplication([])
pencere = login_page()
pencere.show()
app.exec_()
