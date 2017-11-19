from __future__ import absolute_import
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx


class CropEdges:

    @staticmethod
    def distort(video_input, video_output, config):
        clip = VideoFileClip(video_input)
        clip = clip.fx(vfx.crop, x1=5, y1= 5)
        clip.write_videofile(video_output, progress_bar=True, verbose=config.verbose)


if __name__ == '__main__':
    asd = CropEdges()
    asd.distort("/Users/bahadirozavci/Downloads/SampleVideo_360x240_1mb.mp4",
            "/Users/bahadirozavci/Downloads/distorted.mp4")


