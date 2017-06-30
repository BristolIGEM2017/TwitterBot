#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime

plt.style.use('fivethirtyeight')


def create_graph(location, data):
    legend_vals = []
    no_rows = len(set([d['parameter'] for d in data['results']]))
    plt_id = 1
    fig, ax = plt.subplots(nrows=no_rows, ncols=1)
    fig.set_size_inches(15, 10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    for par in set([d['parameter'] for d in data['results']]):
        val = [d['value'] for d in data['results'] if d['parameter'] == par]
        uni = [d['unit'] for d in data['results'] if d['parameter'] == par]
        utc = [datetime.strptime(d['date']['utc'], '%Y-%m-%dT%H:%M:%S.%fZ') for d in data['results'] if d['parameter'] == par]
        # legend_vals.append(par)

        plt.subplot(no_rows, 1, plt_id)
        plt.plot(utc, val)
        plt.legend(par)
        plt.ylabel(uni[0])
        plt_id += 1
        # plt.plot(utc, val)

    # plt.gcf().autofmt_xdate()

    fig.suptitle(location['results'][0]['location'])
    # ax.xlabel('Time')
    # ax.ylabel('Pollution Levels')
    # plt.legend(legend_vals)

    plt.savefig('tweet.png')
    plt.gcf().clear()
