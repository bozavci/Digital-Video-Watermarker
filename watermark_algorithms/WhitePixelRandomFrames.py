from random import randint
import VideoUtils as iu
from PIL import Image
import ConfigurationUtils as configurationUtils


class WhitePixelRandomFrames:

    @staticmethod
    def add_watermark(video, config, aggressiveness):
        aggressiveness = int(100 / aggressiveness)
        dwa = WhitePixelRandomFrames()
        frames_dict = {}
        first = True
        for (time, frame) in video.iter_frames(with_times=True):
            if first or randint(0, aggressiveness) % aggressiveness == 0:
                image_file = iu.extract_image_from_clip(video, time, config)
                frames_dict[time] = image_file
                dwa.encode_image(image_file, config.message)
                return frames_dict
        dwa.add_watermark(video, config, aggressiveness)
        return frames_dict

    @staticmethod
    def extract_message_from_video(video, config):
        dwa = WhitePixelRandomFrames()
        for (time, frame) in video.iter_frames(with_times=True):
            image_file = iu.extract_image_from_clip(video, time, config)
            try:
                msg = configurationUtils.decode(config.password, dwa.decode_image(image_file))
                if msg.startswith(config.message_prefix):
                    return msg[len(config.message_prefix):]
            except:
                pass

    @staticmethod
    def encode_image(image_file, msg):
        img = Image.open(image_file)

        encoded = img.copy()
        width, height = img.size
        limit = 20
        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))
                if r > 255 - limit:
                    r -= limit
                if g > 255 - limit:
                    g -= limit
                if b > 255 - limit:
                    b -= limit

                encoded.putpixel((col, row), (r, g, b))

        length = len(msg)

        """start marker"""
        start_marker = 50
        encoded.putpixel((start_marker, start_marker), (255, 255, 255))
        for i in range(0, length):
            c = msg[i]
            asc = ord(c)
            row = i + start_marker
            col = asc + start_marker
            encoded.putpixel((col, row), (255, 255, 255))
        encoded.save(image_file)

    @staticmethod
    def decode_image(image_file):
        img = Image.open(image_file)
        """
        check the red portion of an image (r, g, b) tuple for
        hidden message characters (ASCII values)
        """
        width, height = img.size
        msg = ""
        start_marker = {}
        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))
                if r == 255 and g == 255 and b == 255:
                    if len(start_marker) == 0:
                        start_marker["col"] = col
                        start_marker["row"] = row
                    else:
                        msg += chr(col - start_marker["col"])

        return msg
