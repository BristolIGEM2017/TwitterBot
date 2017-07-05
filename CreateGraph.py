#!/usr/bin/env python3
import os
import math
from tempfile import mkstemp
from datetime import datetime
from bisect import bisect
import pytz
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tzwhere import tzwhere

tzwhere = tzwhere.tzwhere()

plt.style.use('fivethirtyeight')

title_par = {
    'pm25': 'PM2.5: Particulate Matter 2.5',
    'pm10': 'PM10: Particulate Matter 10',
    'no2': 'NO2: Nitrogen Dioxide',
    'o3': 'O3: Ozone',
    'bc': 'BC: Black Carbon',
    'co': 'CO: Carbon Monoxide',
    'so2': 'SO2: Sulphur Dioxide',
}

pol_lvl = {
    'pm25': [0, 12, 24, 36, 42, 48, 54, 59, 65, 71, math.inf],
    'pm10': [0, 17, 34, 51, 59, 67, 76, 84, 92, 101, math.inf],
    'no2': [0, 68, 135, 201, 268, 335, 401, 468, 535, 601, math.inf],
    'o3': [0, 34, 67, 101, 121, 141, 161, 188, 214, 241, math.inf],
    'so2': [0, 89, 178, 267, 355, 444, 533, 711, 888, 1065, math.inf],
    'co': [],
    'bc': []
}

scale = {
    'o3': 1.9957,
    'no2': 1.9125,
    'so2': 2.6609,
    'co': 0.0011642,
    'bc': 1,
    'pm25': 1,
    'pm10': 1,
}

conversions = {
    k: {
        u'µg/m³': 1,
        u'ppm': 1000 * s,
        u'ppb': s,
    } for k, s in scale.items()
}

colour = {
    1: '#92d04f', 2: '#00b04f', 3: '#006500', 4: '#fad4b4', 5: '#ffc000',
    6: '#e36b09', 7: '#ff0000', 8: '#c00000', 9: '#6f0000', 10: '#000000',
}


def add_subplot(plt, data, par, no_rows, plt_id):

    val = [d['value'] for d in data['results'] if d['parameter'] == par]
    uni = [d['unit'] for d in data['results'] if d['parameter'] == par]
    utc = [datetime.strptime(d['date']['utc'], '%Y-%m-%dT%H:%M:%S.%fZ') for d in data['results'] if d['parameter'] == par]

    val = [x*conversions[par][uni[0]] for x in val]

    plt.subplot(no_rows, 1, plt_id)
    plt.plot(utc, val)

    j = 0
    for x in range(bisect(pol_lvl[par], max(val))):
        if 'co' == par: continue
        if 'bc' == par: continue
        low = pol_lvl[par][j]
        upp = min(pol_lvl[par][j+1], max(val))
        plt.axhspan(low, upp, facecolor=colour[j+1], alpha=0.2)
        j += 1
    plt.title(title_par[par])
    plt.ylabel(u'µg/m³')


def create_graph(location, date, data):
    legend_vals = []
    parameters = list(set([d['parameter'] for d in data['results']]))
    parameters.sort()
    no_rows = len(parameters)
    plt_id = 1

    place = location['results'][0]
    tz_str = tzwhere.tzNameAt(place['coordinates']['latitude'], place['coordinates']['longitude'])
    timezone = pytz.timezone(tz_str)
    date = pytz.utc.localize(date).astimezone(timezone)

    fig, ax = plt.subplots(nrows=no_rows, ncols=1)
    fig.set_size_inches(15, 10)
    fig.subplots_adjust(hspace=0.5)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    for par in parameters:
        add_subplot(plt, data, par, no_rows, plt_id)
        plt_id += 1

    title = '{city}, {country} - {location}'.format(**location['results'][0])
    fig.suptitle(title, fontsize=30)
    fig.text(.5, .92, date.strftime('%d %b %Y %H:%M:%S'), ha='center', fontsize=15)
    fig.text(.5, .01, 'Source: OpenAQ Database', ha='center', fontsize=15)
    handle, filename = mkstemp('.png')
    os.close(handle)
    plt.savefig(filename)
    plt.gcf().clear()
    return filename
