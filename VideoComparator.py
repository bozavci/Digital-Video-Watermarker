from moviepy.editor import VideoFileClip, clips_array, vfx


class VideoComparator:

    @staticmethod
    def compare_videos(video1_path, video2_path, output):
        video1 = VideoFileClip(video1_path).margin(10)
        video2 = VideoFileClip(video2_path).margin(10)

        output_clip = clips_array([[video1], [video2]])
        height = video1.h + video2.h  + 30
        output_clip.resize(height=height).write_videofile(output)


if __name__ == '__main__':
    asd = VideoComparator()
    asd.compare_videos(
                   "/Users/bahadirozavci/Downloads/SampleVideo_360x240_1mb.mp4",
                   "/Users/bahadirozavci/Downloads/watermarked.mp4", "/Users/bahadirozavci/Downloads/compared.mp4")