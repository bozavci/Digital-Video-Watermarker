import os
import imp
import argparse
import shutil
import moviepy.editor as mp


workplace = "/tmp/video_watermarker/"
message_prefix = "WatermarkMessage"
config = {}


def reconstruct_video(video, config, frames_dict):
    frame_duration = 1 / video.fps

    for time in frames_dict:
        image_file = frames_dict[time]
        image_clip = mp.ImageClip(image_file) \
            .set_start(time) \
            .set_duration(frame_duration)

        video = mp.CompositeVideoClip([video, image_clip], ismask=False)

    video.write_videofile(config.output, codec='png')

def apply_watermarking():
    video = mp.VideoFileClip(config.video)

    frames_dict = config.watermarking_algorithm.add_watermark(video, config)
    reconstruct_video(video, config, frames_dict)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', required=True,  help='Full path of video to watermark')
    parser.add_argument('--output', required=True,  help='Full path of output video')
    parser.add_argument('--workplace', default=workplace,  help='Workplace for the library')
    return parser.parse_args()


def init():
    global config
    config = get_arguments()
    if os.path.isdir(config.workplace):
        shutil.rmtree(config.workplace)
    os.mkdir(config.workplace)

    if os.path.isfile(config.output):
        os.remove(config.output)

    config.message = message_prefix + "Nazli bir sapsiktir!"
    config.watermarking_algorithm = \
        imp.load_source('module.name', 'watermark_algorithms/DefaultWatermarkingAlgorithm.py')\
            .DefaultWatermarkingAlgorithm()



def destroy():
    try:
        shutil.rmtree(config.workplace)
    except:
        print ""


if __name__ == '__main__':
    try:
        init()
        apply_watermarking()
    finally:
        destroy()
