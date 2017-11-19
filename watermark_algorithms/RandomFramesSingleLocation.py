import VideoUtils as iu
from PIL import Image
from random import randint
import ConfigurationUtils as configurationUtils

class RandomFramesSingleLocation:

    @staticmethod
    def add_watermark(video, config, aggressiveness):
        aggressiveness = 100 - aggressiveness
        dwa = RandomFramesSingleLocation()
        frames_dict = {}
        first = True
        for (time, frame) in video.iter_frames(with_times=True):
            if first or randint(0, aggressiveness) % aggressiveness == 0:
                image_file = iu.extract_image_from_clip(video, time, config)
                frames_dict[time] = image_file
                dwa.encode_image(image_file, config.message)
                first = False

        return frames_dict

    @staticmethod
    def extract_message_from_video(video, config):
        dwa = RandomFramesSingleLocation()
        for (time, frame) in video.iter_frames(with_times=True):
            if time < 1:
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
        row = 100
        for col in range(width):
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
    def decode_image(image_file):
        img = Image.open(image_file)
        """
        check the red portion of an image (r, g, b) tuple for
        hidden message characters (ASCII values)
        """
        width, height = img.size
        msg = ""
        index = 0
        row = 100
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                # need to add transparency a for some .png files
                r, g, b, a = img.getpixel((col, row))
            # first pixel r value is length of message
            if col == 0:
                length = r
            elif index <= length:
                msg += chr(r)
            index += 1
        return msg
