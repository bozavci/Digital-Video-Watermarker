import VideoUtils as iu
from PIL import Image
from random import randint
import ConfigurationUtils as configurationUtils

class RandomFramesRandomLocation:

    @staticmethod
    def add_watermark(video, config, aggressiveness):
        aggressiveness = int(100 / aggressiveness)
        dwa = RandomFramesRandomLocation()
        frames_dict = {}
        for (time, frame) in video.iter_frames(with_times=True):
            if randint(0, aggressiveness) % aggressiveness == 0:
                image_file = iu.extract_image_from_clip(video, time, config)
                frames_dict[time] = image_file
                col = int(video.w/2) - (len(config.message) / 2)
                row = randint(10, 20) * 10
                dwa.encode_image(image_file, row, col, config.message)
                return
        dwa.add_watermark(video, config, aggressiveness)

    @staticmethod
    def extract_message_from_video(video, config):
        dwa = RandomFramesRandomLocation()
        for (time, frame) in video.iter_frames(with_times=True):
            image_file = iu.extract_image_from_clip(video, time, config)
            try:
                msg = dwa.decode_image(image_file, config)
                if msg.startswith(config.message_prefix):
                    return msg[len(config.message_prefix):]
            except:
                pass

    @staticmethod
    def encode_image(image_file, row, col_start, msg):
        img = Image.open(image_file)
        """
        use the red portion of an image (r, g, b) tuple to
        hide the msg string characters as ASCII values
        red value of the first pixel is used for length of string
        """
        length = len(msg)
        # limit length of message to 255
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return False
        # use a copy of image to hide the text in
        encoded = img.copy()
        width, height = img.size
        index = 0
        color = randint(1, 255)
        encoded.putpixel((col_start-1, row), (color, color, color))
        for col in range(col_start, width):
            r, g, b = img.getpixel((col, row))
            # first value is length of msg
            if col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index - 1]
                asc = ord(c)
            else:
                asc = g
            encoded.putpixel((col, row), (asc, g, b))
            index += 1
        encoded.save(image_file)

    @staticmethod
    def decode_image(image_file, config):
        img = Image.open(image_file)
        """
        check the red portion of an image (r, g, b) tuple for
        hidden message characters (ASCII values)
        """
        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col_start in range(width):
                length = 0
                index = 0
                if col_start-1 > 0:
                    r, g, b = img.getpixel((col_start-1, row))
                    if r > 1 and r == g and g == b:
                        msg = ""
                        for col in range(col_start, width):
                            try:
                                r, g, b = img.getpixel((col, row))
                            except ValueError:
                                # need to add transparency a for some .png files
                                r, g, b, a = img.getpixel((col, row))
                            # first pixel r value is length of message
                            if r == 0:
                                break
                            if length == 0:
                                length = r
                            elif len(msg) == length:
                                break
                            else:
                                msg += chr(r)

                        try:
                            if len(msg) > 0:
                                msg = configurationUtils.decode(config.password, msg)
                                if msg.startswith(config.message_prefix):
                                    return msg
                        except:
                            pass
        return msg
