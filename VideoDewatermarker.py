import os
import imp
import argparse
import shutil
import moviepy.editor as mp

workplace = "/tmp/video_watermarker/"
message_prefix = "WatermarkMessage"
config = {}


def apply_dewatermarking():
    video = mp.VideoFileClip(config.video)

    msg = config.watermarking_algorithm.extract_message_from_video(video, config)
    print msg

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', required=True,  help='Full path of video to dewatermark')
    parser.add_argument('--workplace', default=workplace,  help='Workplace for the library')
    return parser.parse_args()


def init():
    global config
    config = get_arguments()
    if os.path.isdir(config.workplace):
        shutil.rmtree(config.workplace)
    os.mkdir(config.workplace)

    config.message_prefix = message_prefix
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
        apply_dewatermarking()
    finally:
        destroy()