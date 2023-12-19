from PyQt5.QtWidgets import *
from src_py.src_ui.sunucu import Ui_Dialog
from src_py.ses_kaydedici_pyqt5 import sound_record_page
import os 
import numpy as np
import soundfile as sf

from src_py.anlik_erkek_pyqt5 import anlik_erkek_page
from src_py.anlik_kadin_pyqt5 import anlik_kadin_page
from src_py.src.Men_voice import men
from src_py.src.kadin_Sesi import woman
from src_py.src.children_voice import children
from src_py.src.yasli_erkek import make_old_man_voice

from src_py.src_metin.metin_oku import *
from datetime import datetime

class Sunucu_page(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.sunucu = Ui_Dialog()
        self.sunucu.setupUi(self)

        self.background_color = "#404040"
        self.sunucu.pushButton_DosyaSec.clicked.connect(self.dosya_sec)
        self.sunucu.efekt_uygula.clicked.connect(self.radio_buton_efekt)
        self.sunucu.pushButton_MetinKaydet.clicked.connect(self.metni_kaydet)
        self.sunucu.pushButton_MetiNOku.clicked.connect(self.metni_oku)

        self.ses_kaydedici = sound_record_page()
        self.sunucu.pushButton_SesKaydi.clicked.connect(self.ses_kaydet)
        
        self.anlik_erkek = anlik_erkek_page()
        self.sunucu.pushButton_AnlikErkek.clicked.connect(self.anlik_E)

        self.anlik_kadin = anlik_kadin_page()
        self.sunucu.pushButton_AnlikKadin.clicked.connect(self.anlik_K)

        
        self.ses_efekt_liste()
        
    def ses_efekt_liste(self):
        ses_efektler = ["Erkek", "Kadın", "Çocuk","Yaşlı kadın","Yaşlı adam"]

        for efekt in ses_efektler:
            self.sunucu.efekt_combobox.addItem(efekt)
        

    def metni_oku(self):
        secilen_efekt = self.sunucu.efekt_combobox.currentText()
        metin = self.sunucu.textEdit.toPlainText()
        if secilen_efekt =="Erkek":
            
            read_man_thread(metin)

        elif secilen_efekt =="Kadın":
            read_text__woman_thread(metin)

        elif secilen_efekt == "Yaşlı adam":
            read__old_man_t(metin)
            
        elif secilen_efekt == "Yaşlı kadın":
            read__old_woman_t(metin)

        elif secilen_efekt == "Çocuk":
            read_children_thread(metin)

   
    def dosya_sec(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), '(*.wav)')
        self.sunucu.lineEdit_dosyaAdi.setText(fname[0])
    
    def ses_kaydet(self):
        self.ses_kaydedici.show()
    
    def anlik_E(self):
        self.anlik_erkek.show()

    def anlik_K(self):
        self.anlik_kadin.show()



    
    def radio_buton_efekt(self):
        filename =self.sunucu.lineEdit_dosyaAdi.text()
        if not filename :
            print("dosya seçiniz")
        
        else:
            if self.sunucu.radioButton_kadin.isChecked():
                
                try:
                    gender=self.classify(filename)
                    if gender=="Kadın":
                        print("Hata","Zaten kadın sesi")
                    else:
                        woman(filename)
                        print("kadin ses efekti oluşturuldu.")  
                except:
                    print("beklenmedik bir hata oluştu")
            elif self.sunucu.radioButton_Erkek.isChecked():
                
                try:
                    gender=self.classify(filename)
                    if gender=="Erkek":
                        print("Hata","Zaten erkek sesi")
                    else:
                        men(filename)
                        print("erkek ses efekti oluşturuldu.")  
                except:
                    print("beklenmedik bir hata oluştu")

            elif self.sunucu.radioButton_Cocuk.isChecked():
                
                try:
                        children(filename)
                        print("çocuk ses efekti oluşturuldu.")  
                except:
                    print("beklenmedik bir hata oluştu")

            elif self.sunucu.radioButton_yasli_adam.isChecked():
                
                try:
                        make_old_man_voice(filename)
                        print("yaşlı adam ses efekti oluşturuldu.")  
                except:
                    print("beklenmedik bir hata oluştu")
                    

            

    def classify(self,filename):
    
        signal, sample_rate = sf.read(filename)
        signal = np.transpose(signal) # Sinyali transpoze et (kanalları ayır)

        # Ses sinyalini analiz etmek ve sonucu etiketlemek için gereken işlemler burada yapılacak.
        if np.mean(signal[0]) > np.mean(signal[1]):
            gender = "Kadın"
        else:
            gender = "Erkek"

        return gender
    

    def metni_kaydet(self):
        metin = self.sunucu.textEdit.toPlainText()
        tarih = datetime.now().strftime("%Y-%m-%d__%H.%M.%S")
        dosya_adi = f"metin_{tarih}.txt"
        with open(dosya_adi, "w", encoding="utf-8") as dosya:
            dosya.write(metin)
    def get_background_color(self):
        return self.background_color
