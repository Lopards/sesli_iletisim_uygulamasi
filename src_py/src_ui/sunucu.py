# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sunucu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(695, 513)
        Dialog.setMinimumSize(QtCore.QSize(694, 479))
        Dialog.setStyleSheet("color:white;\n"
"background: #404040;")
        self.pushButton_DosyaSec = QtWidgets.QPushButton(Dialog)
        self.pushButton_DosyaSec.setGeometry(QtCore.QRect(30, 40, 93, 31))
        self.pushButton_DosyaSec.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #95A5A6; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"    \n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #ffcc00; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #9932CC; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.pushButton_DosyaSec.setObjectName("pushButton_DosyaSec")
        self.lineEdit_dosyaAdi = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_dosyaAdi.setGeometry(QtCore.QRect(160, 40, 401, 31))
        self.lineEdit_dosyaAdi.setStyleSheet("QComboBox {\n"
"    border: 2px solid #67b26f; /* Kenarlık rengi ve kalınlığı */\n"
"    border-radius: 5px; /* Kenarlık köşe yuvarlama */\n"
"}\n"
"")
        self.lineEdit_dosyaAdi.setObjectName("lineEdit_dosyaAdi")
        self.radioButton_kadin = QtWidgets.QRadioButton(Dialog)
        self.radioButton_kadin.setGeometry(QtCore.QRect(40, 120, 95, 20))
        self.radioButton_kadin.setObjectName("radioButton_kadin")
        self.radioButton_Erkek = QtWidgets.QRadioButton(Dialog)
        self.radioButton_Erkek.setGeometry(QtCore.QRect(40, 170, 95, 20))
        self.radioButton_Erkek.setObjectName("radioButton_Erkek")
        self.radioButton_Cocuk = QtWidgets.QRadioButton(Dialog)
        self.radioButton_Cocuk.setGeometry(QtCore.QRect(40, 220, 95, 20))
        self.radioButton_Cocuk.setObjectName("radioButton_Cocuk")
        self.groupBox_Metin = QtWidgets.QGroupBox(Dialog)
        self.groupBox_Metin.setGeometry(QtCore.QRect(380, 90, 271, 271))
        self.groupBox_Metin.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #393B3B,stop:1 #121313);\n"
"border-radius:20px;")
        self.groupBox_Metin.setObjectName("groupBox_Metin")
        self.pushButton_MetinKaydet = QtWidgets.QPushButton(self.groupBox_Metin)
        self.pushButton_MetinKaydet.setGeometry(QtCore.QRect(90, 150, 93, 31))
        self.pushButton_MetinKaydet.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #95A5A6; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"    \n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #ffcc00; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #9932CC; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.pushButton_MetinKaydet.setObjectName("pushButton_MetinKaydet")
        self.pushButton_MetiNOku = QtWidgets.QPushButton(self.groupBox_Metin)
        self.pushButton_MetiNOku.setGeometry(QtCore.QRect(90, 190, 93, 31))
        self.pushButton_MetiNOku.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #95A5A6; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"    \n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #ffcc00; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #9932CC; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.pushButton_MetiNOku.setObjectName("pushButton_MetiNOku")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_Metin)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 231, 87))
        self.textEdit.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #E7E7E7,stop:1 #D9E6E2);\n"
"color:black;\n"
"border-radius:15px;")
        self.textEdit.setObjectName("textEdit")
        self.efekt_combobox = QtWidgets.QComboBox(self.groupBox_Metin)
        self.efekt_combobox.setGeometry(QtCore.QRect(90, 120, 101, 22))
        self.efekt_combobox.setStyleSheet("QComboBox {\n"
"    border: 2px solid #67b26f; /* Kenarlık rengi ve kalınlığı */\n"
"    border-radius: 5px; /* Kenarlık köşe yuvarlama */\n"
"}\n"
"")
        self.efekt_combobox.setObjectName("efekt_combobox")
        self.groupBox_AnlikSes = QtWidgets.QGroupBox(Dialog)
        self.groupBox_AnlikSes.setGeometry(QtCore.QRect(30, 310, 261, 111))
        self.groupBox_AnlikSes.setObjectName("groupBox_AnlikSes")
        self.pushButton_AnlikErkek = QtWidgets.QPushButton(self.groupBox_AnlikSes)
        self.pushButton_AnlikErkek.setGeometry(QtCore.QRect(80, 10, 93, 31))
        self.pushButton_AnlikErkek.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #95A5A6; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"    \n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #ffcc00; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #9932CC; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.pushButton_AnlikErkek.setObjectName("pushButton_AnlikErkek")
        self.pushButton_AnlikKadin = QtWidgets.QPushButton(self.groupBox_AnlikSes)
        self.pushButton_AnlikKadin.setGeometry(QtCore.QRect(80, 57, 93, 31))
        self.pushButton_AnlikKadin.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #95A5A6; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"    \n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #ffcc00; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #9932CC; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.pushButton_AnlikKadin.setObjectName("pushButton_AnlikKadin")
        self.pushButton_SesKaydi = QtWidgets.QPushButton(Dialog)
        self.pushButton_SesKaydi.setGeometry(QtCore.QRect(590, 37, 93, 31))
        self.pushButton_SesKaydi.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #95A5A6; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"    \n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #ffcc00; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #9932CC; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.pushButton_SesKaydi.setObjectName("pushButton_SesKaydi")
        self.efekt_uygula = QtWidgets.QPushButton(Dialog)
        self.efekt_uygula.setGeometry(QtCore.QRect(190, 257, 93, 31))
        self.efekt_uygula.setStyleSheet("/* Normal durum için */\n"
"QPushButton {\n"
"    background-color: #95A5A6; /* İlk renk */\n"
"    color: #ffffff; /* Metin rengi */\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"/* Üzerine gelindiğinde */\n"
"QPushButton:hover {\n"
"    background-color: #0d730d; /* İkinci renk */\n"
"    \n"
"}\n"
"\n"
"/* Tıklandığında */\n"
"QPushButton:pressed {\n"
"    background-color: #ffcc00; /* Üçüncü renk */\n"
"    color: #000000; /* Tıklandığında metin rengini değiştirin, örneğin siyah yapın */\n"
"}\n"
"\n"
"/* Tıklandıktan sonraki durum için (örneğin, bir toggle düğmesi) */\n"
"QPushButton:checked {\n"
"    background-color: #9932CC; /* Dördüncü renk */\n"
"    color: #ffffff; /* Tıklandıktan sonraki durumda metin rengini değiştirin */\n"
"}")
        self.efekt_uygula.setObjectName("efekt_uygula")
        self.radioButton_yasli_adam = QtWidgets.QRadioButton(Dialog)
        self.radioButton_yasli_adam.setGeometry(QtCore.QRect(40, 260, 121, 20))
        self.radioButton_yasli_adam.setObjectName("radioButton_yasli_adam")
        self.pushButton_DosyaSec.raise_()
        self.lineEdit_dosyaAdi.raise_()
        self.radioButton_kadin.raise_()
        self.radioButton_Erkek.raise_()
        self.radioButton_Cocuk.raise_()
        self.groupBox_AnlikSes.raise_()
        self.pushButton_SesKaydi.raise_()
        self.groupBox_Metin.raise_()
        self.efekt_uygula.raise_()
        self.radioButton_yasli_adam.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_DosyaSec.setText(_translate("Dialog", "Dosya Seç"))
        self.radioButton_kadin.setText(_translate("Dialog", "Kadın Sesi"))
        self.radioButton_Erkek.setText(_translate("Dialog", "Erkek Sesi"))
        self.radioButton_Cocuk.setText(_translate("Dialog", "Çocuk sesi"))
        self.groupBox_Metin.setTitle(_translate("Dialog", "MetinBox"))
        self.pushButton_MetinKaydet.setText(_translate("Dialog", "Metni kaydet"))
        self.pushButton_MetiNOku.setText(_translate("Dialog", "Metni oku"))
        self.groupBox_AnlikSes.setTitle(_translate("Dialog", "Anlik_ses"))
        self.pushButton_AnlikErkek.setText(_translate("Dialog", "Anlık Erkek"))
        self.pushButton_AnlikKadin.setText(_translate("Dialog", "Anlık Kadın"))
        self.pushButton_SesKaydi.setText(_translate("Dialog", "Ses kaydı"))
        self.efekt_uygula.setText(_translate("Dialog", "efekti uygula"))
        self.radioButton_yasli_adam.setText(_translate("Dialog", "Yaşlı Adam sesi"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
