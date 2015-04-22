from __future__ import absolute_import

import json
import pickle
import twitter
import networkx
from pprint import pprint

import config


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

    def graph_json(self, data):
        # print(data['users'][0])
        nodes = [{'name': d.username, 'type': 'person'} for d in data['users']]
        nodes += [{'name': t.status['text'], 'type': 'tweet'} for d in data['users'] for t in d.tweets]
        node_names = [n['name'] for n in nodes]
        # construct links
        links = [{'source': node_names.index(d.username),
                  'target': node_names.index(t.status['text']),
                  'type': 'author'}
                 for d in data['users'] for t in d.tweets]
        print(json.dumps({
            'nodes': nodes,
            'links': links,
        }))

if __name__ == '__main__':
    t = TwitterScraper()
    # t.scrape()
    # pprint([unicode(u) for u in t.load()['users']])
    t.graph_json(t.load())
