#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from tempfile import mkstemp
from PIL import ImageFont, ImageDraw, Image
from AQI import air_quality

import pytz
from tzwhere import tzwhere

tzwhere = tzwhere.tzwhere()

index = {
    1: {'index': 'Low', 'color': (0, 0, 0), 'fill': '#92d04f'},
    2: {'index': 'Low', 'color': (0, 0, 0), 'fill': '#00b04f'},
    3: {'index': 'Low', 'color': (255, 255, 255), 'fill': '#006500'},
    4: {'index': 'Moderate', 'color': (0, 0, 0), 'fill': '#fad4b4'},
    5: {'index': 'Moderate', 'color': (0, 0, 0), 'fill': '#ffc000'},
    6: {'index': 'Moderate', 'color': (0, 0, 0), 'fill': '#e36b09'},
    7: {'index': 'High', 'color': (0, 0, 0), 'fill': '#ff0000'},
    8: {'index': 'High', 'color': (255, 255, 255), 'fill': '#c00000'},
    9: {'index': 'High', 'color': (255, 255, 255), 'fill': '#6f0000'},
    10: {'index': 'Very High', 'color': (255, 255, 255), 'fill': '#000000'},
    'N/A': {'index': 'Unavailable', 'color': (0, 0, 0), 'fill': '#c0c0c0'}
}


def draw_index():
    pass


def create_image(place, date, data):
    img = Image.new('RGBA', (512, 512), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    aqi = air_quality(data)
    title = place['city'] + ', ' + place['country']

    if len(title) > 30:
        title = title[:30] + '...' + ', ' + place['country']

    font_size = 40
    font = ImageFont.truetype('NotoSansUI-Regular.ttf', font_size)

    while font.getsize(title)[0] > 512 - 80:
        font_size -= 1
        font = ImageFont.truetype('NotoSansUI-Regular.ttf', font_size)

    draw.text((40, 15),
              title,
              (0, 0, 0),
              font=font)

    font = ImageFont.truetype('NotoSansUI-Regular.ttf', 25)

    draw.text((40, 60),
              place['location'],
              (0, 0, 0),
              font=font)

    font = ImageFont.truetype('NotoSansUI-Regular.ttf', 20)

    tz_str = tzwhere.tzNameAt(place['coordinates']['latitude'], place['coordinates']['longitude'])
    timezone = pytz.timezone(tz_str)
    date = pytz.utc.localize(date).astimezone(timezone)

    draw.text((40, 110),
              date.strftime('%d %b %Y %H:%M:%S'),
              (0, 0, 0),
              font=font)

    font = ImageFont.truetype('NotoSansUI-Regular.ttf', 25)
    draw.rectangle([(20, 140), (492, 190)],
                   fill=index[aqi['pm25']]['fill'])
    draw.text((40, 150),
              'PM25: ' + index[aqi['pm25']]['index'],
              index[aqi['pm25']]['color'],
              font=font)
    draw.text((440, 150),
              str(aqi['pm25']),
              index[aqi['pm25']]['color'],
              font=font)

    draw.rectangle([(20, 190), (492, 240)],
                   fill=index[aqi['pm10']]['fill'])
    draw.text((40, 200),
              'PM10: ' + index[aqi['pm10']]['index'],
              index[aqi['pm10']]['color'],
              font=font)
    draw.text((440, 200),
              str(aqi['pm10']),
              index[aqi['pm10']]['color'],
              font=font)

    draw.rectangle([(20, 240), (492, 290)],
                   fill=index[aqi['no2']]['fill'])
    draw.text((40, 250),
              'NO2: ' + index[aqi['no2']]['index'],
              index[aqi['no2']]['color'],
              font=font)
    draw.text((440, 250),
              str(aqi['no2']),
              index[aqi['no2']]['color'],
              font=font)

    draw.rectangle([(20, 290), (492, 340)],
                   fill=index[aqi['o3']]['fill'])
    draw.text((40, 300),
              'O3: ' + index[aqi['o3']]['index'],
              index[aqi['o3']]['color'],
              font=font)
    draw.text((440, 300),
              str(aqi['o3']),
              index[aqi['o3']]['color'],
              font=font)

    draw.rectangle([(20, 340), (492, 390)],
                   fill=index[aqi['so2']]['fill'])
    draw.text((40, 350),
              'SO2: ' + index[aqi['so2']]['index'],
              index[aqi['so2']]['color'],
              font=font)
    draw.text((440, 350),
              str(aqi['so2']),
              index[aqi['so2']]['color'],
              font=font)


    font = ImageFont.truetype('NotoSansUI-Regular.ttf', 20)
    draw.text((100, 430), 'Based on the UK Air Quality Index', (0, 0, 0), font=font)
    draw.text((50, 458), 'https://uk-air.defra.gov.uk/air-pollution/daqi', (0, 0, 0), font=font)
    draw.text((100, 485), 'Pollution Bot  -  Bristol iGEM 2017', (0, 0, 0), font=font)

    handle, filename = mkstemp('.png')
    os.close(handle)
    img.save(filename)
    return filename
