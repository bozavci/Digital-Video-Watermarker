import os
import argparse
import shutil
import moviepy.editor as mp
import ConfigurationUtils as configurationUtil
import distutils.util

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

    video.write_videofile(config.output, codec='png', progress_bar=True, verbose=config.verbose)


def apply_watermarking():
    video = mp.VideoFileClip(config.video)

    frames_dict = config.watermarking_algorithm.add_watermark(video, config, config.watermark_algorithm_aggressiveness)
    reconstruct_video(video, config, frames_dict)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', required=True,  help='Full path of video to watermark')
    parser.add_argument('--message', required=True,  help='Message to be watermarked to video')
    parser.add_argument('--password', required=True,  help='Password for recovering message')
    parser.add_argument('--watermark_algorithm', required=True,  help='Algorithm to use for watermarking')
    parser.add_argument('--watermark_algorithm_aggressiveness', type=int, required=True,  help='Algorithms agressiveness between 0 - 100')
    parser.add_argument('--output', required=True,  help='Full path of output video')
    parser.add_argument('--workplace', default=workplace,  help='Workplace for the library')
    parser.add_argument('--verbose', type=distutils.util.strtobool, default='true',  help='Log the outputs')
    return parser.parse_args()


def init():
    global config
    config = get_arguments()
    if os.path.isdir(config.workplace):
        shutil.rmtree(config.workplace)
    os.mkdir(config.workplace)

    if os.path.isfile(config.output):
        os.remove(config.output)

    config.message = configurationUtil.encode(config.password, message_prefix + config.message)
    configurationUtil.set_watermark_algorithm(config)


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
