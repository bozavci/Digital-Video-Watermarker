from __future__ import absolute_import
import imp
import base64


def set_distortion_algorithms(config):
    distortion_algorithms = []
    for distortion_algorithm_str in config.distortion_algorithms.split(','):
        if distortion_algorithm_str == "CropEdges":
            distortion_algorithms.append(imp.load_source
                                                ('module.name', 'distortion_algorithms/CropEdges.py').CropEdges())
        if distortion_algorithm_str == "RGBChanger":
            distortion_algorithms.append(imp.load_source
                                         ('module.name', 'distortion_algorithms/RGBChanger.py').RGBChanger())
        if distortion_algorithm_str == "BlackAndWhite":
            distortion_algorithms.append(imp.load_source
                                         ('module.name', 'distortion_algorithms/BlackAndWhite.py').BlackAndWhite())
    config.distortion_algorithms = distortion_algorithms


def set_watermark_algorithm(config):
    if config.watermark_algorithm == "RandomFramesSingleLocation":
        config.watermarking_algorithm = \
            imp.load_source('module.name', 'watermark_algorithms/RandomFramesSingleLocation.py') \
            .RandomFramesSingleLocation()
    elif config.watermark_algorithm == "RandomFramesRandomLocation":
        config.watermarking_algorithm = \
            imp.load_source('module.name', 'watermark_algorithms/RandomFramesRandomLocation.py') \
            .RandomFramesRandomLocation()
    elif config.watermark_algorithm == "WhitePixelRandomFrames":
        config.watermarking_algorithm = \
            imp.load_source('module.name', 'watermark_algorithms/WhitePixelRandomFrames.py').WhitePixelRandomFrames()
    elif config.watermark_algorithm == "BlackPixelRandomFrames":
        config.watermarking_algorithm = \
            imp.load_source('module.name', 'watermark_algorithms/BlackPixelRandomFrames.py').BlackPixelRandomFrames()


def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)