#!/usr/bin/env python3
import numpy as np
import math

from datetime import datetime, timedelta
from OpenAQ import API

openaq = API()

mw = {'pm25': 0, 'pm10': 0, 'no2': 0, 'o3': 0, 'bc': 0, 'co': 0, 'so2': 0}
time = {'pm25': 24, 'pm10': 24, 'no2': 1, 'o3': 8, 'bc': 8, 'co': 8, 'so2': 1}

pm25 = np.array([0, 11, 12, 23, 24, 35, 36, 41, 42, 46, 47, 53, 54, 58, 59, 64,
                 65, 70, 71, math.inf], dtype=float)
# 24 hour ug/m3
pm10 = np.array([0, 16, 17, 33, 34, 50, 51, 58, 59, 66, 67, 75, 76, 83, 84, 91,
                 92, 100, 101, math.inf], dtype=float)
# 24 hour ug/m3
so2 = np.array([0, 88, 89, 176, 177, 265, 266, 354, 355, 442, 443, 531, 532,
                708, 709, 886, 887, 1063, 1064, math.inf], dtype=float)
# 15 minute ug/m3
no2 = np.array([0, 66, 67, 133, 134, 200, 201, 267, 268, 334, 335, 400, 401,
                467, 468, 534, 535, 600, 601, math.inf], dtype=float)
# 1 hour ug/m3
o3 = np.array([0, 33, 34, 66, 67, 100, 101, 120, 121, 140, 141, 160, 161, 187,
               188, 213, 214, 240, 241, math.inf], dtype=float)
# 8 hour ppm
aqi = np.array([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
               dtype=float)

week = openaq.measurements(location="Bristol St Paul's", limit=1000,
                           date_from=(datetime.now() - timedelta(weeks=1)))


def ugm3_to_ppm(val, mol):
    return (24.45 * (val / 1000)) / mw[mol]


def ppm_to_ugm3(val, mol):
    return 1000 * (0.0409 * val * mw[mol])


def ugm3_to_ppb(val, mol):
    return (24.45 * val) / mw[mol]


def ppb_to_ugm3(val, mol):
    return 0.0409 * val * mw[mol]


def get_index(data, par):
    tmp = [d['value'] for d in data['results'] if d['parameter'] == par and datetime.strptime(d['date']['utc'], '%Y-%m-%dT%H:%M:%S.%fZ') < (datetime.now() - timedelta(hours=time[par]))]
    if tmp == []:
        return 'N/A'
    return round(np.interp(np.mean(tmp), eval(par), aqi))


def air_quality(data):
    pm25_index = get_index(data, 'pm25')
    pm10_index = get_index(data, 'pm10')
    no2_index = get_index(data, 'no2')
    o3_index = get_index(data, 'o3')
    so2_index = get_index(data, 'so2')

    index = {'pm25': pm25_index, 'pm10': pm10_index, 'no2': no2_index,
             'o3': o3_index, 'so2': so2_index}

    return index


air_quality(week)
