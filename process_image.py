import numpy as np
import easygui
import os
import cv2
from PIL import Image, ImageEnhance


class color_channel():
    def __init__(self, filename):
        self.name = filename
        self.img = Image.open(filename)

msg = 'Select image files to use as color data'
types = ['*.bmp','*.eps','*.gif','*.icns','*.ico','*.im','*.jpg','*.jpeg','*.msp',
        '*.pcx','*.png','*.ppm','*.sgi','*.spi','*.tiff','*.webp','*.blp',
        '*.CUR', '*.DCX', '*.DDS', '*.FLI', '*.FLC', '*.FPX', '*.FTEX', '*.GBR',
        '*.GD', '*.IMT', '*.IPTC','*.NAA', '*.MCIDAS', '*.MIC', '*.MPO', '*.PCD',
        '*.PIXAR', '*.PSD', '*.TGA', '*.WAL', '*.XPM']

try:
    easygui.msgbox(msg)
    paths = easygui.fileopenbox(msg, filetypes=types, multiple=True)
    if paths is None:
        raise Exception('Missing color data')
except:
    easygui.exceptionbox()
    raise

channels = dict()
for path in paths:
    chan = easygui.choicebox(
            msg = 'Select color channel for {file}'.format(file=os.path.basename(path)),
            title = 'Select color channel',
            choices = ('Red', 'Blue', 'Green'),
            )
    if chan not in channels:
        channels[chan] = path
    else:
        try:
            raise Exception('Channel already occupied!')
        except:
            easygui.exceptionbox()
            raise

r = color_channel(channels['Red'])
g = color_channel(channels['Green'])
b = color_channel(channels['Blue'])

img_rgb = Image.merge('RGB', (r.img,g.img,b.img))
img_rgb.show()

if easygui.ynbox('Save image?'):
    filename = easygui.filesavebox(filetypes=['*.jpg', '*.png'])
    img_rgb.save(filename)

if easygui.ynbox('Tweak image color?'):
    color_strength = 'Enter percentage multiplier for {color} strength'
    while True:
        r, g, b = img_rgb.split()
        red_strength = easygui.integerbox(
                msg=color_strength.format(color='red'),
                title = 'Red color strength',
                default = 100,
                lowerbound = 0,
                upperbound = None
                )
        r = r.point(lambda i: i * red_strength/100)
        blue_strength = easygui.integerbox(
                msg=color_strength.format(color='blue'),
                title = 'Blue color strength',
                default = 100,
                lowerbound = 0,
                upperbound = None
                )
        b = b.point(lambda i: i * blue_strength/100)
        green_srength = easygui.integerbox(
                msg=color_strength.format(color='green'),
                title = 'Green color strength',
                default = 100,
                lowerbound = 0,
                upperbound = None
                )
        g = g.point(lambda i: i * green_srength/100)
        img_colors = Image.merge('RGB',(r,g,b))
        img_colors.show()
        if easygui.ynbox('Done changing colors?'):
            break
    img_tweak = img_colors

    saturation = 'Enter saturation percentage'
    while True:
        sat = easygui.integerbox(
                msg = saturation,
                title = 'Saturation',
                default = 100,
                lowerbound = 0,
                upperbound = None
                )
        converter = ImageEnhance.Color(img_tweak)
        img_sat = converter.enhance(sat/100)
        img_sat.show()
        if easygui.ynbox('Done changing saturation?'):
            break
    img_tweak = img_sat

    contrast = 'Enter contrast percentage'
    while True:
        con = easygui.integerbox(
                msg = contrast,
                title = 'Contrast',
                default = 100,
                lowerbound = 0,
                upperbound = None
                )
        converter = ImageEnhance.Contrast(img_tweak)
        img_con = converter.enhance(con/100)
        img_con.show()
        if easygui.ynbox('Done changing contrast?'):
            break
    img_tweak = img_con

    brightness = 'Enter brightness percentage'
    while True:
        brt = easygui.integerbox(
                msg = brightness,
                title = 'Brightness',
                default = 100,
                lowerbound = 0,
                upperbound = None
                )
        converter = ImageEnhance.Brightness(img_tweak)
        img_brt = converter.enhance(brt/100)
        img_brt.show()
        if easygui.ynbox('Done changing brightness?'):
            break
    img_tweak = img_brt

    sharpness = 'Enter sharpness percentage'
    while True:
        shp = easygui.integerbox(
                msg = sharpness,
                title = 'Sharpness',
                default = 100,
                lowerbound = 0,
                upperbound = None
                )
        converter = ImageEnhance.Sharpness(img_tweak)
        img_shp = converter.enhance(shp/100)
        img_shp.show()
        if easygui.ynbox('Done changing sharpness?'):
            break
    img_tweak = img_shp
    if easygui.ynbox('Save image?'):
        filename = easygui.filesavebox(filetypes=['*.jpg', '*.png'])
        img_rgb.save(filename)

if easygui.ynbox('Denoise image?'):
    denoise_strength = easygui.integerbox(
            msg= 'Enter denoising strength (rec. 10)',
            title = 'Denoise',
            default = 10,
            lowerbound = 0,
            upperbound = 100
            )
    denoise = cv2.fastNlMeansDenoisingColored(
            src = np.array(img_rgb), 
            dst = None,
            h = denoise_strength,
            hColor = denoise_strength,
            templateWindowSize = 7,
            searchWindowSize = 21
            )
    denoise = Image.fromarray(denoise)
    denoise.show()
    if easygui.ynbox('Save image?'):
        filename = easygui.filesavebox(filetypes=['*.jpg', '*.png'])
        img_rgb.save(filename)
