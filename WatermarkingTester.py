import os
import argparse
import subprocess
import VideoUtils as video_utils
from collections import OrderedDict

workplace = "/tmp/video_watermarker/"
default_watermark_location = "/Users/bahadirozavci/Downloads/watermarked.mp4"
default_distorted_location = "/Users/bahadirozavci/Downloads/distorted.mp4"

message = "bahadirozavci_swe599_Project"
password = "DoNotStealMyProject"


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', required=True,  help='Full path of video to watermark')
    parser.add_argument('--watermark_algorithm', required=True,  help='Algorithm to use for watermarking')
    parser.add_argument('--watermark_algorithm_aggressiveness', type=int, required=True,  help='Algorithms agressiveness between 0 - 100')
    parser.add_argument('--distortion_algorithms', required=True,  help='Distortion Algorithms separated with comma')
    parser.add_argument('--comparison_output', required=True,  help='Full path of output video')
    parser.add_argument('--workplace', default=workplace,  help='Workplace for the library')
    return parser.parse_args()


def watermark(video, watermarking_algorithm, watermark_algorithm_aggressiveness, workplace, message, password):
    command = "python VideoWatermarker.py --video={} --workplace={} --output={} --watermark_algorithm={} \
              --watermark_algorithm_aggressiveness={} --message={} --password={} --verbose=False"\
        .format(video, workplace, default_watermark_location, watermarking_algorithm, watermark_algorithm_aggressiveness
                , message, password)
    os.system(command)


def de_watermark(video, watermarking_algorithm, workplace, password):
    command = "python VideoDewatermarker.py --video={} --workplace={} --watermark_algorithm={} \
              --password={}".format(video, workplace, watermarking_algorithm, password)
    output = subprocess.check_output(command, shell=True)
    return output


def distort_watermarked_video(video, workplace, output, distortion_algorithms):
    command = "python VideoDistorter.py --video={} --workplace={} --output={} --distortion_algorithms={} " \
              "--verbose=False ".format(video, workplace, output, distortion_algorithms)
    output = subprocess.check_output(command, shell=True)
    return output


def create_comparison_video(args):
    video_dict = OrderedDict()
    video_dict["Original"] = args.video
    video_dict["Watermarked : " +
               args.watermark_algorithm + "(" + str(args.watermark_algorithm_aggressiveness) + ")"] \
        = default_watermark_location
    video_dict["Distorted : " + args.distortion_algorithms] = default_distorted_location

    video_utils.compare_videos(video_dict, args.comparison_output, False)


def run_watermarking_test():
    args = get_arguments()
    print("[WatermarkingTester] >>>> Started watermarking")
    watermark(args.video, args.watermark_algorithm, args.watermark_algorithm_aggressiveness, args.workplace, message, password)
    print("[WatermarkingTester] >>>> Started dewatermarking")
    output = de_watermark(default_watermark_location, args.watermark_algorithm, args.workplace, password)
    if output.strip() == message:
        print("[WatermarkingTester] >>>> Watermarking succeeded.")
        print("[WatermarkingTester] >>>> Starting distortion")
        distort_watermarked_video(default_watermark_location, args.workplace, default_distorted_location, args.distortion_algorithms)
        print("[WatermarkingTester] >>>> Distortion completed")
        print("[WatermarkingTester] >>>> Dewatermarking on distorted video")
        output = de_watermark(default_distorted_location, args.watermark_algorithm, args.workplace, password)
        if output.strip() == message:
            print('\033[92m' + "[WatermarkingTester] >>>> Watermark not lost on distorted Video" + '\033[0m')
        else:
            print('\033[91m' + "[WatermarkingTester] >>>> Watermark lost on distorted Video" + '\033[0m')

        print("[WatermarkingTester] >>>> Creating comparison video")
        create_comparison_video(args)
        print("[WatermarkingTester] >>>> Comparison video created!")

    else:
        print("[WatermarkingTester] >>>> Watermarking failed")


if __name__ == '__main__':
    run_watermarking_test()
