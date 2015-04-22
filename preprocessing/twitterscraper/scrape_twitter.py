from __future__ import absolute_import

import pickle
import twitter
import networkx
from pprint import pprint

from . import config


class Tweet(object):
    def __init__(self, user, status):
        self.user = user
        self.status = status

    def __str__(self):
        return self.user.username+': '+unicode(self.status)


class User(object):
    def __init__(self, username):
        self.username = username
        self.tweets = []

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def __str__(self):
        return self.username+': '+unicode([unicode(t) for t in self.tweets])


class TwitterScraper(object):
    def __init__(self):
        self.twitter_api = twitter.Twitter(auth=twitter.OAuth(
            config.twitter['token'],
            config.twitter['token_secret'],
            config.twitter['key'],
            config.twitter['secret'],
        ))

    def _user_timeline(self, username):
        print('Scraping username '+username)
        d = self.twitter_api.statuses.user_timeline(screen_name=username, count=200)
        return d

    def user(self, username):
        u = User(username)
        for s in self._user_timeline(username):
            u.add_tweet(Tweet(u, s))
        return u

    def scrape(self, filename='scraped.pickle'):
        raw_input('About to scrape and overwrite old scrape. '
                  'Press enter to continue.')
        names = [
            '@trywildcard',
            '@jordancooper',
            '@petkanics',
            '@ericxtang',
            '@connormcewen',
            '@marco__castillo',
            '@svenkreiss',
            '@crystallized',
            '@mpolycar',
            '@IsamBatman',
            '@bryanyang',
            '@stephenmeszaros',
            '@bpapa',
            '@maxbulger',
            '@DaveX_87',
            '@komichiewa',
            '@yusmi',
            '@jbigred1',
            '@ffarooq00',
            '@hexedpackets',
            '@_andlum',
            '@ryandawidjan',
            '@karsenthil',
            '@khoi',
        ]
        with open(filename, 'wb') as f:
            pickle.dump({'users': [t.user(n) for n in names]}, f)
            # pickle.dump({'users': [t.user(names[0])]}, f)

    def load(self, filename='scraped.pickle'):
        with open(filename, 'rb') as f:
            return pickle.load(f)

if __name__ == '__main__':
    t = TwitterScraper()
    # t.scrape()
    pprint([unicode(u) for u in t.load()['users']])
