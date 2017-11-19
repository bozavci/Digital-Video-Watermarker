from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, clips_array, ColorClip


def extract_image_from_clip(clip, t, config):
    file_name = config.workplace + "/frame" + str(t) + ".png"
    clip.save_frame(file_name, t, withmask=True)
    return file_name


def write_text_to_video(video_path, text):
    clip = VideoFileClip(video_path)

    text_clip = TextClip(text, font='Amiri-regular',  color='white',fontsize=12)\
        .set_duration(clip.duration)\
        .set_pos(("center", "top"))

    final_clip = CompositeVideoClip([clip, text_clip])
    return final_clip


def compare_videos(video_dict, output, verbose):

    height = 0
    videos = []

    for video_label in video_dict:
        video = write_text_to_video(video_dict[video_label], video_label).margin(10)
        videos.append(video)
        height += video.h + 10

    black_clip = ColorClip(videos[0].size, (0,0,0), duration=videos[0].duration)

    arr = [[videos[0], videos[1]], [black_clip, videos[2] ]]
    output_clip = clips_array(arr)
    output_clip.resize(height=height).write_videofile(output, progress_bar=True, verbose=verbose)