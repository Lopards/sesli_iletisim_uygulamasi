# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'secim_ekrani.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Secim(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(408, 205)
        MainWindow.setMinimumSize(QtCore.QSize(408, 235))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SUNUCU_buton = QtWidgets.QPushButton(self.centralwidget)
        self.SUNUCU_buton.setGeometry(QtCore.QRect(70, 120, 93, 28))
        self.link = QtWidgets.QPushButton(self.centralwidget)
        self.link.setGeometry(QtCore.QRect(100, 180, 200, 28))
        self.link.setObjectName("link")
        self.SUNUCU_buton.setObjectName("SUNUCU_buton")
        self.CLIENT_buton = QtWidgets.QPushButton(self.centralwidget)
        self.CLIENT_buton.setGeometry(QtCore.QRect(250, 120, 93, 28))
        self.CLIENT_buton.setObjectName("CLIENT_buton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 40, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 408, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SUNUCU_buton.setText(_translate("MainWindow", "Doktor"))
        self.CLIENT_buton.setText(_translate("MainWindow", "Öğrenci"))
        self.link.setText(_translate("MainWindow", "created by Emirhan"))
        self.label.setText(_translate("MainWindow", " Tarafını seç !"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Secim()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
