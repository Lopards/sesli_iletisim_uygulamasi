import numpy as np
from scipy.io import wavfile

def make_old_man_voice(audio_file):
   
    sample_rate, audio = wavfile.read(audio_file)

    # Ses dosyasının tonunu değiştir.
    audio = change_pitch(audio, -11)

    # Ses dosyasının hızını değiştir.
    audio = change_speed(audio, 1.3)

    # Veri türünü uygun şekilde dönüştür.
    if audio.dtype == np.complex64 or audio.dtype == np.complex128:
        audio = audio.real.astype(np.float32)

    # Dönüştürülmüş ses dosyasını kaydet.
    wavfile.write("yaşlı_adam.wav", sample_rate, audio)

def change_pitch(audio, n_semitones):
   

    # Ses dosyasını frekans alanına dönüştür. fourier 
    frequencies = np.fft.fft(audio)

    # Frekansları belirtilen yarıton kadar kaydır.
    frequencies = frequencies * np.exp( 2 * np.pi * n_semitones / 8)

    # Frekansları zaman alanına geri dönüştür.
    audio = np.fft.ifft(frequencies)

    # Tonu değiştirilmiş ses dosyasını döndür.
    return audio

def change_speed(audio, rate):
    """
   hızını belirtilen oranda değiştirir.

    Args:
        audio: Hızı değiştirilecek ses dosyası.
        rate: Hız değişikliği oranı.

    Returns:
        Hızı değiştirilmiş ses dosyası.
    """

    # Ses dosyasını zaman alanına dönüştür.
    samples = np.arange(audio.size)

    # Yeni örnek noktalarını hesapla.
    new_samples = np.linspace(0, samples[-1], int(samples[-1] * rate) + 1)

    # Yeni örnek noktalarını tam sayıya dönüştür.
    new_samples = new_samples.astype(int)

    # Yeni örnek noktalarını kullanarak ses dosyasını yeniden örnekle.
    new_audio = audio[new_samples]

    # Hızı değiştirilmiş ses dosyasını döndür.
    return new_audio





#C:/rise_teknoloji/kaydedilen_Erkek_ses.wav
