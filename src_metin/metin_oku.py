import threading
from responsive_voice import ResponsiveVoice


def read_woman(metin):
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.FEMALE, rate=0.47, pitch=0.5, vol=1)
 
        
def read_text__woman_thread(metin):
       
        threading.Thread(target=read_woman, args=(metin,)).start()



def read_man_thread(metin):

            threading.Thread(target=read_man, args=(metin,)).start()

def read_man(metin):
        
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.MALE, rate=0.47, pitch=0.36, vol=1)

def read_old_man(metin):
        
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.MALE, rate=0.33, pitch=0.25, vol=1)
        

def read__old_man_t(metin):

        threading.Thread(target=read_old_man, args=(metin,)).start()


def read_old_woman(metin):
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.FEMALE, rate=0.36, pitch=0.28, vol=1)
        
       

def read__old_woman_t(metin):

        threading.Thread(target=read_old_woman, args=(metin,)).start()

def read_children(metin):
        engine = ResponsiveVoice()
        engine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH)
        engine.say(metin, gender=ResponsiveVoice.FEMALE, rate=0.45, pitch=0.75, vol=0.5)
 
        
def read_children_thread(metin):

        threading.Thread(target=read_children, args=(metin,)).start()