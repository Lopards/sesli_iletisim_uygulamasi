# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_erkek.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Server_erkek(object):
    def setupUi(self, Server_erkek):
        Server_erkek.setObjectName("Server_erkek")
        Server_erkek.resize(1061, 553)
        Server_erkek.setMinimumSize(QtCore.QSize(1061, 553))
        self.centralwidget = QtWidgets.QWidget(Server_erkek)
        self.centralwidget.setObjectName("centralwidget")
        self.metin_islemleri_frame = QtWidgets.QFrame(self.centralwidget)
        self.metin_islemleri_frame.setGeometry(QtCore.QRect(330, 130, 341, 331))
        self.metin_islemleri_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.metin_islemleri_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.metin_islemleri_frame.setObjectName("metin_islemleri_frame")
        self.Metin_yeri_4 = QtWidgets.QPlainTextEdit(self.metin_islemleri_frame)
        self.Metin_yeri_4.setGeometry(QtCore.QRect(20, 20, 301, 151))
        self.Metin_yeri_4.setPlainText("")
        self.Metin_yeri_4.setObjectName("Metin_yeri_4")
        self.sesli_yaz_buton_4 = QtWidgets.QPushButton(self.metin_islemleri_frame)
        self.sesli_yaz_buton_4.setGeometry(QtCore.QRect(60, 190, 93, 28))
        self.sesli_yaz_buton_4.setObjectName("sesli_yaz_buton_4")
        self.Gonder_buton_4 = QtWidgets.QPushButton(self.metin_islemleri_frame)
        self.Gonder_buton_4.setGeometry(QtCore.QRect(120, 250, 93, 28))
        self.Gonder_buton_4.setObjectName("Gonder_buton_4")
        self.sesli_yaz_durdur_buton_4 = QtWidgets.QPushButton(self.metin_islemleri_frame)
        self.sesli_yaz_durdur_buton_4.setGeometry(QtCore.QRect(180, 190, 131, 28))
        self.sesli_yaz_durdur_buton_4.setObjectName("sesli_yaz_durdur_buton_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(800, 110, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(90, 30, 101, 16))
        self.label_4.setObjectName("label_4")
        self.Ses_islemleri_frame = QtWidgets.QFrame(self.centralwidget)
        self.Ses_islemleri_frame.setGeometry(QtCore.QRect(30, 130, 251, 331))
        self.Ses_islemleri_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Ses_islemleri_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Ses_islemleri_frame.setObjectName("Ses_islemleri_frame")
        self.Baslat_buton_4 = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.Baslat_buton_4.setGeometry(QtCore.QRect(20, 30, 93, 28))
        self.Baslat_buton_4.setObjectName("Baslat_buton_4")
        self.Durdur_buton_4 = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.Durdur_buton_4.setGeometry(QtCore.QRect(130, 30, 93, 28))
        self.Durdur_buton_4.setObjectName("Durdur_buton_4")
        self.Ses_al_buton_4 = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.Ses_al_buton_4.setGeometry(QtCore.QRect(60, 100, 93, 28))
        self.Ses_al_buton_4.setObjectName("Ses_al_buton_4")
        self.Ses_a_devaml_buton_4 = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.Ses_a_devaml_buton_4.setGeometry(QtCore.QRect(10, 160, 101, 28))
        self.Ses_a_devaml_buton_4.setObjectName("Ses_a_devaml_buton_4")
        self.Ses_al_dur_buton_4 = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.Ses_al_dur_buton_4.setGeometry(QtCore.QRect(120, 160, 93, 28))
        self.Ses_al_dur_buton_4.setObjectName("Ses_al_dur_buton_4")
        self.baglantiyi_kes_buton_4 = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.baglantiyi_kes_buton_4.setGeometry(QtCore.QRect(70, 290, 121, 28))
        self.baglantiyi_kes_buton_4.setObjectName("baglantiyi_kes_buton_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 110, 101, 16))
        self.label.setObjectName("label")
        self.ip_tara = QtWidgets.QPushButton(self.centralwidget)
        self.ip_tara.setGeometry(QtCore.QRect(210, 50, 93, 28))
        self.ip_tara.setObjectName("ip_tara")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 110, 111, 16))
        self.label_2.setObjectName("label_2")
        self.ip_adres = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_adres.setGeometry(QtCore.QRect(50, 50, 151, 22))
        self.ip_adres.setObjectName("ip_adres")
        self.hoparor_secim_frame = QtWidgets.QFrame(self.centralwidget)
        self.hoparor_secim_frame.setGeometry(QtCore.QRect(710, 130, 281, 331))
        self.hoparor_secim_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hoparor_secim_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hoparor_secim_frame.setObjectName("hoparor_secim_frame")
        self.hoparlo_sec_button_4 = QtWidgets.QPushButton(self.hoparor_secim_frame)
        self.hoparlo_sec_button_4.setGeometry(QtCore.QRect(90, 290, 93, 28))
        self.hoparlo_sec_button_4.setObjectName("hoparlo_sec_button_4")
        self.hoparlor_list = QtWidgets.QListView(self.hoparor_secim_frame)
        self.hoparlor_list.setGeometry(QtCore.QRect(10, 10, 256, 201))
        self.hoparlor_list.setObjectName("hoparlor_list")
        self.baglanti_kur = QtWidgets.QPushButton(self.centralwidget)
        self.baglanti_kur.setGeometry(QtCore.QRect(330, 50, 93, 28))
        self.baglanti_kur.setObjectName("baglanti_kur")
        Server_erkek.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Server_erkek)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1061, 26))
        self.menubar.setObjectName("menubar")
        Server_erkek.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Server_erkek)
        self.statusbar.setObjectName("statusbar")
        Server_erkek.setStatusBar(self.statusbar)

        self.retranslateUi(Server_erkek)
        QtCore.QMetaObject.connectSlotsByName(Server_erkek)

    def retranslateUi(self, Server_erkek):
        _translate = QtCore.QCoreApplication.translate
        Server_erkek.setWindowTitle(_translate("Server_erkek", "MainWindow"))
        self.sesli_yaz_buton_4.setText(_translate("Server_erkek", "Sesli yaz"))
        self.Gonder_buton_4.setText(_translate("Server_erkek", "Gönder"))
        self.sesli_yaz_durdur_buton_4.setText(_translate("Server_erkek", "Sesli yazmayı durdur"))
        self.label_3.setText(_translate("Server_erkek", "Hoparlör seçimi"))
        self.label_4.setText(_translate("Server_erkek", "IP Adresin"))
        self.Baslat_buton_4.setText(_translate("Server_erkek", "Başlat"))
        self.Durdur_buton_4.setText(_translate("Server_erkek", "Durdur"))
        self.Ses_al_buton_4.setText(_translate("Server_erkek", "Ses Al"))
        self.Ses_a_devaml_buton_4.setText(_translate("Server_erkek", "Ses al Devam Et"))
        self.Ses_al_dur_buton_4.setText(_translate("Server_erkek", "Ses al dur"))
        self.baglantiyi_kes_buton_4.setText(_translate("Server_erkek", "Baglantıyı kes"))
        self.label.setText(_translate("Server_erkek", "Ses İşlemleri"))
        self.ip_tara.setText(_translate("Server_erkek", "tara"))
        self.label_2.setText(_translate("Server_erkek", "Metin Gönderme"))
        self.hoparlo_sec_button_4.setText(_translate("Server_erkek", "Hoparlör seç"))
        self.baglanti_kur.setText(_translate("Server_erkek", "bağlantı kur"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Server_erkek = QtWidgets.QMainWindow()
    ui = Ui_Server_erkek()
    ui.setupUi(Server_erkek)
    Server_erkek.show()
    sys.exit(app.exec_())
