#!/usr/bin/env python3
from datetime import datetime, timedelta
import numpy as np
from OpenAQAPI import API

openaq = API()

time = {'pm25': 24, 'pm10': 24, 'no2': 1, 'o3': 8, 'bc': 8, 'co': 8, 'so2': 1}

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

tables = {
    'pm25': np.array([0, 11, 12, 23, 24, 35, 36, 41, 42, 46, 47, 53, 54, 58, 59, 64,
                      65, 70, 71, float('inf')], dtype=float),
    'pm10': np.array([0, 16, 17, 33, 34, 50, 51, 58, 59, 66, 67, 75, 76, 83, 84, 91,
                      92, 100, 101, float('inf')], dtype=float),
    'so2': np.array([0, 88, 89, 176, 177, 265, 266, 354, 355, 442, 443, 531, 532,
                     708, 709, 886, 887, 1063, 1064, float('inf')], dtype=float),
    'no2': np.array([0, 66, 67, 133, 134, 200, 201, 267, 268, 334, 335, 400, 401,
                     467, 468, 534, 535, 600, 601, float('inf')], dtype=float),
    'o3': np.array([0, 33, 34, 66, 67, 100, 101, 120, 121, 140, 141, 160, 161, 187,
                    188, 213, 214, 240, 241, float('inf')], dtype=float),
}
aqi = np.array([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
               dtype=float)

def get_index(data, par):
    tmp = [d['value'] for d in data['results'] if d['parameter'] == par and datetime.strptime(d['date']['utc'], '%Y-%m-%dT%H:%M:%S.%fZ') < (datetime.now() - timedelta(hours=time[par]))]
    if tmp == []:
        return 'N/A'
    unit = [d['unit'] for d in data['results'] if d['parameter'] == par]
    tmp = [x*conversions[par][unit[0]] for x in tmp]
    return round(np.interp(np.mean(tmp), tables[par], aqi))


def air_quality(data):
    pm25_index = get_index(data, 'pm25')
    pm10_index = get_index(data, 'pm10')
    no2_index = get_index(data, 'no2')
    o3_index = get_index(data, 'o3')
    so2_index = get_index(data, 'so2')

    index = {'pm25': pm25_index, 'pm10': pm10_index, 'no2': no2_index,
             'o3': o3_index, 'so2': so2_index}

    return index
