from __future__ import absolute_import

from moviepy.editor import VideoFileClip
from random import randint
import VideoUtils as iu
from PIL import Image
import moviepy.editor as mp


class PepperAndSalt:

    @staticmethod
    def distort(video_input, video_output, config):
        clip = VideoFileClip(video_input)

        frame_duration = 1 / clip.fps

        dwa = PepperAndSalt()
        for (time, frame) in clip.iter_frames(with_times=True):
            if randint(0, 10) % 10 == 0:
                image_file = iu.extract_image_from_clip(clip, time, config)
                dwa.encode_image(image_file)
                image_clip = mp.ImageClip(image_file) \
                    .set_start(time) \
                    .set_duration(frame_duration)

                clip = mp.CompositeVideoClip([clip, image_clip], ismask=False)
        clip.write_videofile(video_output, codec='png',  progress_bar=True, verbose=config.verbose)

    @staticmethod
    def encode_image(image_file):
        img = Image.open(image_file)

        encoded = img.copy()
        width, height = img.size

        for row in range(0, height):
            for col in range(0, width):
                if randint(0, 1000) % 1000 == 0:
                    color = 255
                    if randint(0, 2) % 2 == 0:
                        color = 0
                    encoded.putpixel((col, row), (color, color, color))
        encoded.save(image_file)