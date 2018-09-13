import colorsys
from image_fns import *
from PIL import Image
import os
import glob


def get_color_dict(image):
    img_width = image.size[0]

    if image.mode in ('RGBA', 'LA', 'RGB') or (image.mode == 'P' and 'transparency' in image.info):
        simple_img = image.convert('P', palette=Image.ADAPTIVE, colors=256)
        pixels = list(simple_img.convert('RGBA').getdata())

        color_dict = dict()

        for r, g, b, a in pixels:
            pixel = (r, g, b)
            if pixel in color_dict:
                color_dict[pixel] += 1
            else:
                color_dict[pixel] = 1

        ratio = sum(color_dict.values()) / img_width

        for item in color_dict:
            color_dict[item] = color_dict[item] // ratio

        return color_dict


def get_colors(color_dict):
    colors = list(color_dict.keys())

    try:
        colors.sort(key=lambda rgb: colorsys.rgb_to_hls(*rgb))
    finally:
        try:
            colors.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
        finally:
            return colors


def create_new_image(image, color_dict):
    img_height = image.size[1]
    img_width = image.size[0]
    bar_width = img_width
    bar_height = int(bar_width // 15)
    actual_width = int(sum(color_dict.values()))
    actual_height = int(actual_width // 15)

    new_img = Image.new('RGB', (img_width, img_height + bar_height))
    bar_img = Image.new('RGB', (actual_width, actual_height))

    col = 0

    colors = get_colors(color_dict)

    for item in colors:
        if color_dict[item]:
            width = int(color_dict[item])
            temp_img = Image.new('RGB', (width, actual_height), item)
            bar_img.paste(temp_img, (col, 0))
            col += width
    bar_img = resize(bar_img, img_width)
    new_img.paste(image)
    new_img.paste(bar_img, (0, img_height))

    return new_img


def convert_file(open_path, save_path):
    img = Image.open(open_path)
    rotated = False
    if img.size[1] > img.size[0]:
        img = rotate_port_to_land(img)
        rotated = True
    color_dict = get_color_dict(img)
    new_img = create_new_image(img, color_dict)
    new_img.save(save_path)

    if rotated:
        img = Image.open(save_path)
        img = rotate_land_to_port(img)
        img.save(save_path)


def main():
    folder = os.path.abspath(os.path.join('.', 'image'))
    items = glob.glob(os.path.join(folder, '*'))

    for item in items:
        file_extension = os.path.splitext(item)[1]
        filename = os.path.splitext(os.path.basename(item))[0]
        save_file = os.path.abspath(os.path.join('.', 'image', 'output', filename + '.png'))
        if file_extension == '.jpg' or file_extension == '.jpeg' or file_extension == '.png':
            convert_file(item, save_file)


if __name__ == '__main__':
    main()
