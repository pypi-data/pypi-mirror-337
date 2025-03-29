import os

import cv2
import numpy as np
from publicmodel.common import animation_progress_bar, auto_line_wrap

from EasyCryptographer import FormatError, one_layer_encryption, second_level_decryption


class Encryptor:
    def __init__(self, text, output_file, frame_size=(100, 100), fps=10):
        self.text = one_layer_encryption(text)
        self.output_file = output_file
        self.frame_size = frame_size
        self.fps = fps

        # Check if the output file extension is compatible with FFV1
        self.check_compatible_extension()

    def check_compatible_extension(self):
        # List of compatible extensions for FFV1
        compatible_extensions = ['.avi', '.mkv']
        file_extension = os.path.splitext(self.output_file)[1].lower()
        if file_extension not in compatible_extensions:
            raise FormatError(
                f"File extension '{file_extension}' is not compatible with FFV1 codec. Use one of {compatible_extensions}."
            )

    def text_to_color(self, text):
        # Convert each character to a color (R, G, B)
        colors = []
        for char in text:
            ascii_val = ord(char)
            colors.append((ascii_val, ascii_val, ascii_val))  # Use the same value for R, G, and B channels
        return colors

    def save_video(self):
        colors = self.text_to_color(self.text)
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        video_writer = cv2.VideoWriter(self.output_file, fourcc, self.fps, self.frame_size)

        for color in colors:
            frame = np.zeros((self.frame_size[1], self.frame_size[0], 3), dtype=np.uint8)
            frame[:] = color
            video_writer.write(frame)

        video_writer.release()


class Decryptor:
    def __init__(self, input_file):
        self.input_file = input_file

    def color_to_text(self, colors):
        text = ''
        for color in colors:
            r, g, b = color
            text += chr(r)  # Use only the red channel
        return text

    def video_to_text(self):
        video_capture = cv2.VideoCapture(self.input_file)
        colors = []

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            # Assume the color is uniform across the frame
            color = frame[0, 0]
            colors.append(tuple(color))

        video_capture.release()
        text = self.color_to_text(colors)
        return second_level_decryption(text)


if __name__ == '__main__':
    text = (
        'This innovative encryption and decryption method uses video frames to securely encode and decode text. The'
        ' Encryptor class applies a one-layer encryption algorithm to the input text, converting each character '
        'into a color value based on its ASCII value. These color values create video frames saved in a file using '
        'the FFV1 codec. The Decryptor class reads the video frames, extracts the color values, and converts them '
        'back into characters. The extracted text undergoes a second-level decryption to retrieve the original '
        'message. This approach combines text encryption with video encoding, offering a unique and secure '
        'solution for protecting sensitive information.'
    )

    try:
        encryptor = Encryptor(
            text,
            '../../generated_items/video/hide_to_video_lite.avi',
            (1024, 768),
            10
        )
        animation_progress_bar(
            "Encrypting...",
            None,
            0.25,
            encryptor.save_video,
            "process",
        )
        print("Encryption is complete.")
    except FormatError as e:
        print(f"Error: {e}")

    decryptor = Decryptor('../../generated_items/video/hide_to_video_lite.avi')
    extracted_text = animation_progress_bar(
        "Decrypting...",
        None,
        0.25,
        decryptor.video_to_text,
        "process",
    )
    try:
        extracted_text = auto_line_wrap(extracted_text, 100, True)
    except AttributeError:
        pass

    print("Decryption is completed.\n")
    print("Decrypted text:")
    print(f"{extracted_text}")  # Print the decrypted text with quotes to visualize spaces
