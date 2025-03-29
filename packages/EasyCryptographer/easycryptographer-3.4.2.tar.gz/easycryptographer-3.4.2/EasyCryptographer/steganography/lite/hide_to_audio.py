import numpy as np
from publicmodel.common import auto_line_wrap, animation_progress_bar
from scipy.io.wavfile import write, read
from scipy.signal import get_window

from EasyCryptographer import one_layer_encryption, second_level_decryption


class Encryptor:
    def __init__(self, text):
        self.text = one_layer_encryption(text)
        self.base_frequency = 440
        self.duration_per_char = 0.5
        self.sample_rate = 44100
        self.amplitude = 1.0  # 增加一个参数来控制幅度

    def text_to_audio(self):
        audio_data = np.array([], dtype=np.float32)
        for char in self.text:
            char_code = ord(char)
            frequency = self.base_frequency + char_code
            t = np.linspace(0, self.duration_per_char, int(self.sample_rate * self.duration_per_char), endpoint=False)
            tone = self.amplitude * np.sin(2 * np.pi * frequency * t).astype(np.float32)  # 使用 self.amplitude 来控制幅度
            audio_data = np.concatenate((audio_data, tone))
        return audio_data

    def save_audio(self, filename):
        audio_data = self.text_to_audio()
        write(filename, self.sample_rate, audio_data)


class Decryptor:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.base_frequency = 440
        self.duration_per_char = 0.5
        self.sample_rate = 44100

    def audio_to_text(self):
        sample_rate, audio_data = read(self.audio_path)
        num_samples_per_char = int(self.sample_rate * self.duration_per_char)
        text = ""
        for i in range(0, len(audio_data), num_samples_per_char):
            segment = audio_data[i:i + num_samples_per_char]
            frequency = self.detect_frequency(segment, sample_rate)
            char_code = int(round(frequency - self.base_frequency))
            text += chr(char_code)
        return second_level_decryption(text)

    def detect_frequency(self, segment, sample_rate):
        window = get_window('blackman', len(segment))  # 使用布莱克曼窗
        segment = segment * window
        fft_result = np.fft.fft(segment, n=len(segment) * 4)  # 使用零填充来提高频率分辨率
        frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
        peak_frequency = abs(frequencies[np.argmax(np.abs(fft_result))])
        return peak_frequency


if __name__ == '__main__':
    text = (
        "Encryption using audio frequencies hides information within sound. Each text character is converted to its "
        "ASCII code and mapped to a unique frequency by adding it to a base frequency, usually 440 Hz. Sine waves are "
        "generated for each character and combined into a WAV file. For decryption, the audio file is divided into "
        "segments, each representing one character. The dominant frequency of each segment is detected using FFT, "
        "converted back to ASCII code, and transformed into text. This method adds an extra layer of security, "
        "offering a unique approach to steganography."
    )
    # text = one_layer_encryption(text)
    # print(text)
    # print(second_level_decryption(text))

    encryptor = Encryptor(
        text,
    )
    animation_progress_bar(
        "Encrypting...",
        None,
        0.25,
        encryptor.save_audio,
        "process",
        '../../generated_items/audio/hide_to_audio_lite.wav'
    )
    print("Encryption is complete.")

    decryptor = Decryptor('../../generated_items/audio/hide_to_audio_lite.wav')
    extracted_text = animation_progress_bar(
        "Decrypting...",
        None,
        0.25,
        decryptor.audio_to_text,
        "process",
    )
    try:
        extracted_text = auto_line_wrap(extracted_text, 100, True)
    except AttributeError:
        pass

    print("Decryption is completed.\n")
    print("Decrypted text:")
    print(extracted_text)
