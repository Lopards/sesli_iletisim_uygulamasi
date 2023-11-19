# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_erkek_son.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1021, 750)
        Form.setMinimumSize(QtCore.QSize(1021, 750))
        Form.setStyleSheet("color:white;\n"
"background: #404040;")
        self.settings = QtCore.QSettings('YourCompany', 'YourApp')
        self.settingsButton = QtWidgets.QPushButton('', Form)
        #self.settingsButton.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.settingsButton.clicked.connect(self.openSettings)
        self.settingsButton.setGeometry(QtCore.QRect(780, 180, 139, 31))
        self.settingsButton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")


        self.ip_tara = QtWidgets.QPushButton(Form)
        self.ip_tara.setGeometry(QtCore.QRect(210, 60, 91, 31))
        self.ip_tara.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.ip_tara.setObjectName("ip_tara")
        self.Ses_islemleri_frame = QtWidgets.QFrame(Form)
        self.Ses_islemleri_frame.setGeometry(QtCore.QRect(30, 150, 251, 241))
        self.Ses_islemleri_frame.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #393B3B,stop:1 #121313);\n"
"color:white;\n"
"border-radius:20px;\n"
"")
        self.Ses_islemleri_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Ses_islemleri_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Ses_islemleri_frame.setObjectName("Ses_islemleri_frame")
        self.Baslat_buton = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.Baslat_buton.setGeometry(QtCore.QRect(70, 30, 121, 31))
        self.Baslat_buton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.Baslat_buton.setObjectName("Baslat_buton")
        self.Ses_a_devaml_buton = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.Ses_a_devaml_buton.setGeometry(QtCore.QRect(70, 90, 121, 31))
        self.Ses_a_devaml_buton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.Ses_a_devaml_buton.setObjectName("Ses_a_devaml_buton")
        self.baglantiyi_kes_buton = QtWidgets.QPushButton(self.Ses_islemleri_frame)
        self.baglantiyi_kes_buton.setGeometry(QtCore.QRect(70, 150, 121, 31))
        self.baglantiyi_kes_buton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.baglantiyi_kes_buton.setObjectName("baglantiyi_kes_buton")
        self.hoparor_secim_frame = QtWidgets.QFrame(Form)
        self.hoparor_secim_frame.setGeometry(QtCore.QRect(700, 180, 291, 291))
        self.hoparor_secim_frame.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #393B3B,stop:1 #121313);\n"
"border-radius:20px;")
        self.hoparor_secim_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hoparor_secim_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hoparor_secim_frame.setObjectName("hoparor_secim_frame")
        self.hoparlo_sec_button = QtWidgets.QPushButton(self.hoparor_secim_frame)
        self.hoparlo_sec_button.setGeometry(QtCore.QRect(100, 240, 93, 31))
        self.hoparlo_sec_button.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.hoparlo_sec_button.setObjectName("hoparlo_sec_button")
        self.hoparlor_liste = QtWidgets.QListView(self.hoparor_secim_frame)
        self.hoparlor_liste.setGeometry(QtCore.QRect(20, 30, 256, 201))
        self.hoparlor_liste.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #E7E7E7,stop:1 #D9E6E2);\n"
"color:black;\n"
"border-radius:15px;")
        self.hoparlor_liste.setObjectName("hoparlor_liste")
        self.metin_islemleri_frame = QtWidgets.QFrame(Form)
        self.metin_islemleri_frame.setGeometry(QtCore.QRect(330, 140, 341, 331))
        self.metin_islemleri_frame.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #393B3B,stop:1 #121313);\n"
"color:white;\n"
"border-radius:20px;")
        self.metin_islemleri_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.metin_islemleri_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.metin_islemleri_frame.setObjectName("metin_islemleri_frame")
        self.sesli_yaz_buton = QtWidgets.QPushButton(self.metin_islemleri_frame)
        self.sesli_yaz_buton.setGeometry(QtCore.QRect(50, 180, 93, 31))
        self.sesli_yaz_buton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.sesli_yaz_buton.setObjectName("sesli_yaz_buton")
        self.Gonder_buton = QtWidgets.QPushButton(self.metin_islemleri_frame)
        self.Gonder_buton.setGeometry(QtCore.QRect(120, 270, 93, 31))
        self.Gonder_buton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.Gonder_buton.setObjectName("Gonder_buton")
        self.sesli_yaz_durdur_buton = QtWidgets.QPushButton(self.metin_islemleri_frame)
        self.sesli_yaz_durdur_buton.setGeometry(QtCore.QRect(180, 180, 131, 31))
        self.sesli_yaz_durdur_buton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.sesli_yaz_durdur_buton.setObjectName("sesli_yaz_durdur_buton")
        self.metin_yeri = QtWidgets.QTextEdit(self.metin_islemleri_frame)
        self.metin_yeri.setGeometry(QtCore.QRect(40, 20, 261, 121))
        self.metin_yeri.setStyleSheet("color:black;\n"
"background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #E7E7E7,stop:1 #D9E6E2);\n"
"border-radius:15px;")
        self.metin_yeri.setObjectName("metin_yeri")
        self.efek_combobox = QtWidgets.QComboBox(self.metin_islemleri_frame)
        self.efek_combobox.setGeometry(QtCore.QRect(120, 230, 101, 21))
        self.efek_combobox.setStyleSheet("QComboBox {\n"
"    border: 2px solid #67b26f; /* Kenarlık rengi ve kalınlığı */\n"
"    border-radius: 5px; /* Kenarlık köşe yuvarlama */\n"
"}\n"
"")
        self.efek_combobox.setObjectName("efek_combobox")
        self.Dosya_gonder_buton = QtWidgets.QPushButton(self.metin_islemleri_frame)
        self.Dosya_gonder_buton.setGeometry(QtCore.QRect(220, 270, 61, 31))
        self.Dosya_gonder_buton.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.Dosya_gonder_buton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("dosya_gonder_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Dosya_gonder_buton.setIcon(icon)
        self.Dosya_gonder_buton.setObjectName("Dosya_gonder_buton")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 470, 341, 241))
        self.groupBox.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #393B3B,stop:1 #121313);\n"
"border-radius:20px;")
        self.groupBox.setObjectName("groupBox")
        self.ogr_hoparlor_liste_ac = QtWidgets.QPushButton(self.groupBox)
        self.ogr_hoparlor_liste_ac.setGeometry(QtCore.QRect(90, 20, 141, 31))
        self.ogr_hoparlor_liste_ac.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.ogr_hoparlor_liste_ac.setObjectName("ogr_hoparlor_liste_ac")
        self.ogrenci_hoparlor_liste = QtWidgets.QListView(self.groupBox)
        self.ogrenci_hoparlor_liste.setGeometry(QtCore.QRect(10, 60, 321, 141))
        self.ogrenci_hoparlor_liste.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #E7E7E7,stop:1 #D9E6E2);\n"
"border-radius:20px;\n"
"color:black;")
        self.ogrenci_hoparlor_liste.setObjectName("ogrenci_hoparlor_liste")
        self.ogrenci_hoparlor_sec = QtWidgets.QPushButton(self.groupBox)
        self.ogrenci_hoparlor_sec.setGeometry(QtCore.QRect(120, 210, 93, 31))
        self.ogrenci_hoparlor_sec.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.ogrenci_hoparlor_sec.setObjectName("ogrenci_hoparlor_sec")
        self.hoparlor_liste_ac = QtWidgets.QPushButton(Form)
        self.hoparlor_liste_ac.setGeometry(QtCore.QRect(780, 140, 131, 31))
        self.hoparlor_liste_ac.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.hoparlor_liste_ac.setObjectName("hoparlor_liste_ac")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(440, 120, 111, 16))
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.baglanti_kur = QtWidgets.QPushButton(Form)
        self.baglanti_kur.setGeometry(QtCore.QRect(330, 60, 93, 31))
        self.baglanti_kur.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #0099cc; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"\n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #0066cc; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #0066cc; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.baglanti_kur.setObjectName("baglanti_kur")
        self.oda_kod_yeri = QtWidgets.QLabel(Form)
        self.oda_kod_yeri.setGeometry(QtCore.QRect(880, 20, 71, 21))
        self.oda_kod_yeri.setStyleSheet("    color:rgb(255, 255, 255)")
        self.oda_kod_yeri.setText("")
        self.oda_kod_yeri.setObjectName("oda_kod_yeri")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 120, 101, 16))
        self.label.setObjectName("label")
        self.ip_adres = QtWidgets.QLineEdit(Form)
        self.ip_adres.setGeometry(QtCore.QRect(50, 60, 151, 31))
        self.ip_adres.setStyleSheet("\n"
"")
        self.ip_adres.setObjectName("ip_adres")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(804, 20, 71, 21))
        self.label_6.setStyleSheet("    color:rgb(255, 255, 255)")
        self.label_6.setObjectName("label_6")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(800, 120, 101, 16))
        self.label_3.setStyleSheet("    color:rgb(255, 255, 255)")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(90, 40, 101, 16))
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)



        self.settings_dialog = QtWidgets.QDialog()

        # Pencere başlığı ve boyutu
        self.settings_dialog.setWindowTitle("Ayarlar")
        self.settings_dialog.setGeometry(800, 400, 700, 400)
        self.settings_dialog.setStyleSheet("color:white;\n"
"background: #404040;")
        self.hoparor_secim_frame.setParent(self.settings_dialog)
        self.hoparor_secim_frame.setGeometry(QtCore.QRect(20, 20, 291, 291))

        # "ogrenci_hoparlor_liste" ve "hoparlor_liste" widget'larını yeni pencereye taşı
        self.groupBox.setParent(self.settings_dialog)
        self.groupBox.setGeometry(QtCore.QRect(320, 30, 341, 241))

        # Yeni pencereyi gizle
        self.settings_dialog.hide()




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ip_tara.setText(_translate("Form", "tara"))
        self.Baslat_buton.setText(_translate("Form", "Mikrofon"))
        self.Ses_a_devaml_buton.setText(_translate("Form", "Kulaklık"))
        self.baglantiyi_kes_buton.setText(_translate("Form", "Baglantıyı kes"))
        self.hoparlo_sec_button.setText(_translate("Form", "Hoparlör seç"))
        self.sesli_yaz_buton.setText(_translate("Form", "Sesli yaz"))
        self.Gonder_buton.setText(_translate("Form", "Gönder"))
        self.sesli_yaz_durdur_buton.setText(_translate("Form", "Sesli yazmayı durdur"))
        self.groupBox.setTitle(_translate("Form", "Öğrenci tarafının Hoparlörünü seçin"))
        self.ogr_hoparlor_liste_ac.setText(_translate("Form", "Hoparlör Listesini Aç"))
        self.ogrenci_hoparlor_sec.setText(_translate("Form", "Seç"))
        self.hoparlor_liste_ac.setText(_translate("Form", "Hoparlör Listesini Aç"))
        self.label_2.setText(_translate("Form", "Metin Gönderme"))
        self.baglanti_kur.setText(_translate("Form", "bağlantı kur"))
        self.label.setText(_translate("Form", "Ses İşlemleri"))
        self.label_6.setText(_translate("Form", "Oda Kodu:"))
        self.label_3.setText(_translate("Form", "Hoparlör seçimi"))
        self.label_4.setText(_translate("Form", "IP Adresin"))


    def openSettings(self):
        # Ayarlar penceresini oluştur
        self.settings_dialog.show()
        """settings_dialog = QtWidgets.QDialog()

        # Pencere başlığı ve boyutu
        settings_dialog.setWindowTitle("Ayarlar")
        settings_dialog.setGeometry(100, 100, 400, 300)

        # "ogrenci_hoparlor_liste" ve "hoparlor_liste" widget'larını yeni pencereye taşı
        self.hoparor_secim_frame.setParent(settings_dialog)
        self.hoparor_secim_frame.setGeometry(QtCore.QRect(20, 30, 291, 291))
        self.hoparor_secim_frame.show()

        self.groupBox.setParent(settings_dialog)
        self.groupBox.setGeometry(QtCore.QRect(320, 30, 341, 241))
        self.groupBox.show()

        # Yeni pencereyi göster
        settings_dialog.exec_()"""


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
