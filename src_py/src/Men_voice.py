import numpy as np
import soundfile as sf
from scipy import signal

def men(file):
    audio_data, sample_rate = sf.read(file)
    pitch_shift_factor = 1.3  # Örnek bir öteleme faktörü, isteğe göre değiştirilebilir

    audio_data_float32 = audio_data.astype(np.float32)
    buffer = audio_data_float32.tobytes()
    audio_data_from_buffer = np.frombuffer(buffer, dtype=np.float32)
    shifted_audio_data = signal.resample(audio_data_from_buffer, int(len(audio_data) * pitch_shift_factor))

    output_file = "erkek.wav"
    sf.write(output_file, shifted_audio_data, sample_rate)
    

# 'man' fonksiyonunu çağırarak ses dosyasını işleyebiliriz
