import ffmpeg
from publicmodel.common import ord2, chr2
from pydub import AudioSegment

__version__ = "3.4.2"

if __name__ != "__main__":
    from .convention.AEAD import AEAD_method
    from .convention.AES import AES_method
    from .convention.Blowfish import Blowfish_method
    from .convention.CAST5 import CAST5_method
    from .convention.Fernet import Fernet_method
    from .convention.RC4 import RC4_method
    from .convention.RSA import RSA_method
    from .steganography import lite
    from .steganography import pro

    __all__ = [
        '__version__',
        'one_layer_encryption',
        'second_level_decryption',
        'AudioSegment',
        'AEAD_method',
        'AES_method',
        'Blowfish_method',
        'CAST5_method',
        'string_to_binary',
        'Fernet_method',
        'RC4_method',
        'RSA_method',
        'lite',
        'pro',
        'binary_to_string',
        'segment_binary',
        'convert_audio_format',
        'convert_video_format',
        'SecurityLevelError',
        'ImageError',
        'ParameterError',
        'UnknownError',
        'FormatError',
    ]


def one_layer_encryption(text):
    try:
        return ord2(text)
    except ValueError:
        pass


def second_level_decryption(text):
    try:
        return chr2(text)
    except ValueError:
        pass


def string_to_binary(s):
    # 将字符串转换为二进制表示，使用 UTF-8 编码
    return ''.join(format(ord(char), '016b') for char in s)


def binary_to_string(b):
    # 将二进制表示转换回字符串
    chars = [chr(int(b[i:i + 16], 2)) for i in range(0, len(b), 16)]
    return ''.join(chars)


def segment_binary(b):
    original_str = binary_to_string(b)

    # 计算每个字符的平均二进制长度
    segment_length = len(b) // len(original_str)

    # 分段
    segments = [b[i:i + segment_length] for i in range(0, len(b), segment_length)]
    return segments


def convert_audio_format(input_file_path, target_format, output_file_path):
    # Load the audio file
    audio = AudioSegment.from_file(input_file_path)

    # Export the audio file in the target format
    audio.export(output_file_path, format=target_format)


def convert_video_format(input_file_path, target_format, output_file_path):
    stream = ffmpeg.input(input_file_path)
    stream = ffmpeg.output(stream, output_file_path, format=target_format)

    # Run the ffmpeg command
    ffmpeg.run(stream)


class SecurityLevelError(Exception):
    """Throw an exception when the security value is incorrect."""
    pass


class ImageError(Exception):
    """Throw an exception when the image is incorrect."""
    pass


class ParameterError(Exception):
    """Throw an exception when the parameter is incorrect."""
    pass


class UnknownError(Exception):
    """Throw an exception when the unknown error occurs."""
    pass


class FormatError(Exception):
    """Throw an exception when the format is incorrect."""
    pass


if __name__ == "__main__":
    convert_video_format(
        'generated_items/video/hide_to_video_lite.avi',
        'mp4',
        'generated_items/video/hide_to_video_lite.mp4'
    )
