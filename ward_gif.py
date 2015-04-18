__author__ = 'Eddie'

from PIL import Image
from visvis.vvmovie import images2swf, images2avi
import os


def ward_gif():

    file_names = [x for x in os.listdir('C:/Users/Eddie/PycharmProjects/WardScan/frames') if os.path.splitext(x)[1] in ('.png')]
    images = [Image.open('C:/Users/Eddie/PycharmProjects/WardScan/frames/{}'.format(f)) for f in file_names]

    file_name = "ward_gif.swf"
    images2swf.writeSwf(file_name, images, duration=0.2)

ward_gif()