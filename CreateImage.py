#!/usr/bin/env python3
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

bg_no = '1'
shadowcolor = "#333333"


def shadow_text(draw, x, y, text, colour=(0, 0, 0), font=None, fill='#333333'):
    draw.text((x-1, y), text, font=font, fill=fill)
    draw.text((x+1, y), text, font=font, fill=fill)
    draw.text((x, y+1), text, font=font, fill=fill)
    draw.text((x, y-1), text, font=font, fill=fill)
    draw.text((x, y), text, colour, font=font)


def create_image():
    font = ImageFont.truetype('Roboto-Regular.ttf', 40)
    img = Image.new('RGBA', (512, 512), (255, 255, 255))
    # img = Image.open('assets/bg'+bg_no+'.jpg')
    draw = ImageDraw.Draw(img)

    shadow_text(draw, 20, 20, 'Bristol, St. Pauls', font=font, fill=shadowcolor)

    font = ImageFont.truetype('Roboto-Regular.ttf', 25)
    shadow_text(draw, 40, 130, 'NO2: Moderate', font=font)
    shadow_text(draw, 40, 180, 'SO2: Very Unhealthy', font=font)
    shadow_text(draw, 40, 230, '03: Good', font=font)
    shadow_text(draw, 40, 280, 'CO: Unhealthy', font=font)
    shadow_text(draw, 40, 330, 'BC: Unhealthy for Sensitive Groups', font=font)
    shadow_text(draw, 40, 380, 'PM25: Hazardous', font=font)
    shadow_text(draw, 40, 430, 'PM10: Moderate', font=font)

    font = ImageFont.truetype('Roboto-Regular.ttf', 20)
    shadow_text(draw, 100, 490, 'Pollution Bot  -  Bristol iGEM 2017', font=font)

    '''
    draw.text((50, 200), 'NO2: High', (255, 255, 255), font=font)
    draw.text((50, 300), 'O3: Medium', (255, 255, 255), font=font)
    draw.text((50, 400), 'SO2: Low', (255, 255, 255), font=font)
    draw.text((300, 200), 'BC: Low', (255, 255, 255), font=font)
    draw.text((300, 300), 'PM25: High', (255, 255, 255), font=font)
    draw.text((300, 400), 'PM10: Medium', (255, 255, 255), font=font)
    draw.text((0, 580), 'Pollution Bot   -   Bristol iGEM 2017', (255, 255, 255), font=font)

    '''

    draw = ImageDraw.Draw(img)
    draw = ImageDraw.Draw(img)
    img.save('bg'+bg_no+'.png')


create_image()
