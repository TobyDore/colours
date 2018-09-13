from PIL import Image


def resize(image, new_width):
    (old_width, old_height) = image.size
    aspect_ratio = old_height / old_width
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image


def rotate_land_to_port(image):
    img_width = image.size[0]
    img_height = image.size[1]
    img2 = Image.new('RGB', (img_width, img_width))
    img2.paste(image, (0, int((img_width - img_height) / 2)))
    img3 = Image.new('RGB', (img_height, img_width))
    img3.paste(img2.rotate(90), (-int((img_width - img_height) / 2), 0))
    return img3


def rotate_port_to_land(image):
    img_width = image.size[0]
    img_height = image.size[1]
    img2 = Image.new('RGB', (img_height, img_height))
    img2.paste(image, (int((img_height - img_width) / 2), 0))
    img3 = Image.new('RGB', (img_height, img_width))
    img3.paste(img2.rotate(270), (0, -int((img_height - img_width) / 2)))
    return img3
