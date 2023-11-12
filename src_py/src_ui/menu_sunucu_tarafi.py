from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QWidget
from src_py.server_erkek_pyqt5 import server_erkek_page
from src_py.server_kadin_pyqt5 import server_kadin_page
from src_py.sunucu_pyqt5 import Sunucu_page

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.menus = {}

    def initUI(self):
        self.setWindowTitle("Doktor - Menü")
        self.setGeometry(100, 100, 400, 300)

        menubar = self.menuBar()
        menu = menubar.addMenu("Seçenekler")

        ses_islemleri = QAction("ses işlemleri", self)
        ses_islemleri.triggered.connect(lambda: self.show_menu(ses_islemleri))
        menu.addAction(ses_islemleri)

        interkom_e = QAction("interkom (erkek)", self)
        interkom_e.triggered.connect(lambda: self.show_menu(interkom_e))
        menu.addAction(interkom_e)

        interkom_k = QAction("interkom (kadın)", self)
        interkom_k.triggered.connect(lambda: self.show_menu(interkom_k))
        menu.addAction(interkom_k)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

    def show_menu(self, menu_action):
        # Menüyü ismine göre al
        menu_name = menu_action.text()
        menu = self.menus.get(menu_name)

        # Eğer mevcut menü varsa göster, yoksa oluştur
        if not menu:
            if menu_name == "ses işlemleri":
                menu = Sunucu_page()
            elif menu_name == "interkom (erkek)":
                menu = server_erkek_page()
            elif menu_name == "interkom (kadın)":
                menu = server_kadin_page()

            self.layout.addWidget(menu)
            self.menus[menu_name] = menu

        # Diğer menüleri gizle
        for existing_menu_name, existing_menu in self.menus.items():
            if existing_menu_name != menu_name:
                existing_menu.hide()

        # Mevcut menüyü göster
        menu.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()


"""if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()"""
