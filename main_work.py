from PyQt5.QtWidgets import QApplication
from  secim_ekran_pyqt5 import login_page

app = QApplication([])
pencere = login_page()
pencere.show()
app.exec_()


