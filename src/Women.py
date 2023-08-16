import parselmouth
from parselmouth.praat import call
from IPython.display import Audio




def women(dosya):   
    sound = parselmouth.Sound(dosya) # sound nesnesi 'dosya' nın özelliklerini ve değerlerini temsil eder

    Audio(data=sound.values, rate=sound.sampling_frequency) # ses dosyasının değerleri ve örnekleme frekansları oluşturulur 


    manipulation = call(sound, "To Manipulation", 0.03, 75, 600)# sound nesnesi üzzerinde "to manipulatıion işlemi çağırılır. sesin analinizini yapıp manipülasyon için gerekli verileri toplar"
                                           # zaman adımı min.hz max.hz 
    print(type(manipulation))#kontrol amaçlı

    pitch_tier = call(manipulation, "Extract pitch tier") # extract ifadesiyle pitch tıer nesnesi çağırılır bu sesin perde bilgisini temsil eder

    call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax,3) # perde bilgileri verilen değerle çarpılır. max-min maksimım zaman değerlerini temsil eder

    call([pitch_tier, manipulation], "Replace pitch tier")# bu nesneleri bir listeye alarak replace p.tier çağırılr bu işlemde yukardaki bilgiler yer değiştirilir
    yeni_ses = call(manipulation, "Get resynthesis (overlap-add)")*1.5# burada değiştirilmiş sesi  yesni_ses olarak yeniden birleştirir

    Audio(data=yeni_ses.values, rate=yeni_ses.sampling_frequency)

    yeni_ses.save("kadin_sesi.wav", "WAV")
    Audio(filename="kadin_sesi.wav")
    


