#!/usr/bin/env python3
import tweepy
import os
import pytz
import re
import settings

from CreateGraph import create_graph
from CreateImage import create_image
from datetime import datetime, timedelta
from OpenAQAPI import API

CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET

times = {
    'h': timedelta(hours=1),
    'd': timedelta(days=1),
    "w": timedelta(weeks=1),
}


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, tweet):
        if 'graph' in tweet.text:
            self.tweet_graph(tweet)
        else:
            self.tweet_image(tweet)

    def on_error(self, status_code):
        if status_code == 420:
            print(status_code)
            return False

    def tweet_image(self, tweet):
        print('I will tweet an Image')
        coords = self.get_location(tweet)
        if coords is None:
            self.tweet_help(tweet)
            return
        coords = str(coords[1]) + ',' + str(coords[0])
        location = openaq.locations(coordinates=coords,
                                    nearest=1,
                                    radius=100
                                    )
        from_date = datetime.now(tz=pytz.UTC)-timedelta(hours=25)
        air_data = openaq.measurements(location=location['results'][0]['location'],
                                       date_from=from_date,
                                       limit=1000
                                       )
        img = create_image(location['results'][0],
                           tweet.created_at,
                           air_data)
        twitter.update_with_media(img,
                                  '@{}'.format(tweet.author.screen_name),
                                  tweet.id)
        os.remove(img)

    def tweet_graph(self, tweet):
        print('I will tweet a graph')
        coords = self.get_location(tweet)
        if coords is None:
            self.tweet_help(tweet)
            return
        coords = str(coords[1]) + ',' + str(coords[0])
        location = openaq.locations(coordinates=coords,
                                    nearest=1,
                                    radius=100
                                    )

        pattern = r'(\d+)\s*(w(eek)?|d(ay)?|h(our)?)s?'
        text = re.search(pattern, tweet.text.lower())

        if text is None:
            self.tweet_help()
            return
        print(text.groups())
        time_delta = times[text.group(2)[0]] * int(text.group(1))

        from_date = datetime.now(tz=pytz.UTC)-time_delta
        print(location['results'][0]['location'])
        air_data = openaq.measurements(location=location['results'][0]['location'],
                                       date_from=from_date.strftime('%FT%T'),
                                       limit=1000
                                       )
        print(from_date.strftime('%FT%T'))
        img = create_graph(location, air_data)
        twitter.update_with_media(img,
                                  '@{}'.format(tweet.author.screen_name),
                                  tweet.id)
        os.remove(img)

    def tweet_help(self, tweet):
        pass

    def get_location(self, tweet):
        if tweet.place is not None:
            coords = tweet.place.bounding_box.coordinates[0]
            coords = [sum(x)/len(x) for x in zip(*coords)]
        elif tweet.coordinates is not None:
            coords = tweet.coordinates.coordinates
        else:
            return None
        return coords


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    openaq = API()
    twitter = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    stream = tweepy.Stream(auth=auth, listener=MyStreamListener())

    stream.userstream('pollution_bot')
    stream.filter(track=[])
