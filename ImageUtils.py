from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def extract_image_from_clip(clip, t, config):
    file_name = config.workplace + "/frame" + str(t) + ".png"
    clip.save_frame(file_name, t, withmask=True)
    return file_name


def make_image_grayscale(image_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("arial.ttf", 16)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((0, 0), "Mahmut", (255, 255, 255), font=font)
    img.save(image_path)
