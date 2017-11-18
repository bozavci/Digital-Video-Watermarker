import ImageUtils as iu
from PIL import Image


class DefaultWatermarkingAlgorithm:

    @staticmethod
    def add_watermark(video, config):
        dwa = DefaultWatermarkingAlgorithm()
        frames_dict = {}
        for (time, frame) in video.iter_frames(with_times=True):
            image_file = iu.extract_image_from_clip(video, time, config)
            frames_dict[time] = image_file
            dwa.encode_image(image_file, config.message)
            return frames_dict

        return frames_dict

    @staticmethod
    def extract_message_from_video(video, config):
        dwa = DefaultWatermarkingAlgorithm()
        for (time, frame) in video.iter_frames(with_times=True):
            if time < 1:
                image_file = iu.extract_image_from_clip(video, time, config)
                msg = dwa.decode_image(image_file)
                if msg.startswith(config.message_prefix):
                    return msg

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
        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index - 1]
                    asc = ord(c)
                else:
                    asc = g
                encoded.putpixel((col, row), (r, asc, b))
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
        for row in range(height):
            for col in range(width):
                try:
                    r, g, b = img.getpixel((col, row))
                except ValueError:
                    # need to add transparency a for some .png files
                    r, g, b, a = img.getpixel((col, row))
                # first pixel r value is length of message
                if row == 0 and col == 0:
                    length = g
                elif index <= length:
                    msg += chr(g)
                index += 1
        return msg

if __name__ == '__main__':
    dwAlgo = DefaultWatermarkingAlgorithm()

    msg = dwAlgo.decode_image("/Users/bahadirozavci/Desktop/frame0.0.png")

    print(msg)
