__author__ = 'Eddie'

from PIL import Image, ImageDraw
import json

# constants
d = 8
x_off, y_off = 570, 420
scale = 30


def open_json():
    f = open('data.json')
    data = json.loads(f.read())["data"]
    f.close()
    map_wards(data)


def set_frames(data):
    size = 0
    image = []
    for e in range(len(data)):
        if size <= round(data[e]["time"] / 60000):
            size = round(data[e]["time"] / 60000)

    for x in range(size):
        image.append(Image.open('mapping.png').resize((512, 512)))

    return image


def map_wards(data):
    accumulator = 1

    frames = set_frames(data)
    for e in range(len(data)):
        index = round(data[e]["time"] / 60000) - 1
        im = Image.new('RGBA', (512, 512))
        draw = ImageDraw.Draw(im, "RGBA")

        if data[e]["team"] == 100:
            color = (0, 0, 126, 200)
        elif data[e]["team"] == 200:
            color = (126, 0, 0, 200)

        x = data[e]["position"]["x"] + x_off
        y = data[e]["position"]["y"] + y_off

        draw.ellipse([x / scale - d, y / scale - d, x / scale + d, y / scale + d], fill=color)
        del draw

        frames[index] = Image.alpha_composite(frames[index], im)

    for image in frames:
        canvas = Image.open('minimap-mh.png').convert("RGBA")
        Image.alpha_composite(canvas, image.transpose(Image.FLIP_TOP_BOTTOM)).save(
            "C:/Users/Eddie/PycharmProjects/WardScan/frames/{}.png".format(accumulator), "PNG")
        accumulator += 1


open_json()