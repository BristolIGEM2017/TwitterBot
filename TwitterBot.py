#!/usr/bin/env python3
import os
import re
from datetime import datetime, timedelta
import tweepy
import pytz
import settings
from CreateGraph import create_graph
from CreateImage import create_image
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
        if tweet.author.screen_name == 'pollution_bot':
            return
        elif hasattr(tweet, 'retweeted_status'):
            return
        elif tweet.in_reply_to_status_id:
            return
        try:
            if 'graph' in tweet.text.lower():
                self.tweet_graph(tweet)
            else:
                self.tweet_image(tweet)
        except KeyboardInterrupt as _:
            raise KeyboardInterrupt
        except Exception as e:
            print(e)
            self.tweet_error(tweet)


    def on_error(self, status_code):
        if status_code == 420:
            print(status_code)
            return False

    def on_timeout(self):
        print('Timeout at {}'.format(datetime.now()))

    def on_disconnect(self, notice):
        print('Disconnected at {} : {}'.format(datetime.now(), notice))
        return False

    def tweet_image(self, tweet):
        coords = self.get_location(tweet)
        if coords is None:
            self.tweet_help(tweet)
            return
        coords = str(coords[1]) + ',' + str(coords[0])
        location = openaq.locations(coordinates=coords,
                                    nearest=5
                                   )
        from_date = datetime.now(tz=pytz.UTC)-timedelta(hours=25)
        for x in location['results']:
            air_data = openaq.measurements(location=x['location'],
                                           date_from=from_date.strftime('%FT%T'),
                                           limit=10000
                                          )
            if air_data['results']:
                break

        if air_data['results'] == []:
            self.tweet_no_data(tweet)
            return
        img = create_image(location['results'][0],
                           tweet.created_at,
                           air_data)
        msg = ' Here is your pollution data!'
        twitter.update_with_media(img,
                                  '@{}'.format(tweet.author.screen_name) + msg,
                                  in_reply_to_status_id=tweet.id)
        os.remove(img)

    def tweet_graph(self, tweet):
        coords = self.get_location(tweet)
        if coords is None:
            self.tweet_help(tweet)
            return
        coords = str(coords[1]) + ',' + str(coords[0])
        location = openaq.locations(coordinates=coords,
                                    nearest=5,
                                   )

        pattern = r'([\d.,]+)\s*(w(eek)?|d(ay)?|h(our)?)s?'
        text = re.search(pattern, tweet.text.lower())

        if text is None:
            time_delta = timedelta(days=7)
        else:
            time_delta = times[text.group(2)[0]] * float(text.group(1).replace(',', '.'))

        from_date = datetime.now(tz=pytz.UTC)-time_delta

        for x in location['results']:
            air_data = openaq.measurements(location=x['location'],
                                           date_from=from_date.strftime('%FT%T'),
                                           limit=10000
                                          )
            if air_data['results']:
                break

        if air_data['results'] == []:
            self.tweet_no_data(tweet)
            return
        img = create_graph(location, tweet.created_at, air_data)
        msg = ' Here is a graph of your pollution data!'
        twitter.update_with_media(img,
                                  '@{}'.format(tweet.author.screen_name) + msg,
                                  in_reply_to_status_id=tweet.id)
        os.remove(img)

    def tweet_help(self, tweet):
        msg = ' You must specify a location on your tweet'
        twitter.update_status('@{}'.format(tweet.author.screen_name) + msg,
                              in_reply_to_status_id=tweet.id)

    def tweet_no_data(self, tweet):
        msg = u' I\'m sorry \U0001F625, there\'s no available data near you.'
        twitter.update_status('@{}'.format(tweet.author.screen_name) + msg,
                              in_reply_to_status_id=tweet.id)

    def tweet_error(self, tweet):
        msg = u' Oh dear, I think something went wrong! \U0001F631 \u26A0'
        twitter.update_status('@{}'.format(tweet.author.screen_name) + msg,
                              in_reply_to_status_id=tweet.id)

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
