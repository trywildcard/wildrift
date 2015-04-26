from __future__ import absolute_import

import json
import pickle
import twitter
import datetime
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

    def filter_tweets(self, data, recency=None):
        if not recency:
            recency = datetime.datetime.now()-datetime.timedelta(days=60)
        # print(datetime.datetime.strptime(data['users'][0].tweets[0].status['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
        for u in data['users']:
            # for t in u.tweets:
            #     print(datetime.datetime.strptime(t.status['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            u.tweets = [t for t in u.tweets
                        if datetime.datetime.strptime(t.status['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > recency]

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
        # pprint(unicode(data['users'][0].tweets[0].status['entities']['user_mentions']))
        nodes = [{'name': d.username,
                  'type': 'person',
                  'followers_count': d.tweets[0].status['user']['followers_count'] if d.tweets else 0,
                  'description': d.tweets[0].status['user']['description'] if d.tweets else '',
                  'profile_image_url': d.tweets[0].status['user']['profile_image_url'] if d.tweets else ''}
                 for d in data['users']]
        nodes += [{'name': '@'+m['screen_name'],
                   'type': 'person-non-wildcard'}
                  for d in data['users'] for t in d.tweets
                  for m in t.status['entities']['user_mentions']]
        nodes += [{'name': t.status['text'],
                   'type': 'tweet',
                   'favorite_count': t.status['favorite_count'],
                   'retweet_count': t.status['retweet_count']}
                  for d in data['users'] for t in d.tweets]
        # deduplicate and build node_names
        node_names = []
        nodes_new = []
        for n in nodes:
            if n['name'] in node_names:
                continue
            node_names.insert(0, n['name'])
            nodes_new.insert(0, n)
        nodes = nodes_new
        # construct links
        links = [{'source': node_names.index(d.username),
                  'target': node_names.index(t.status['text']),
                  'type': 'author' if not t.status['retweeted'] else 'retweet'}
                 for d in data['users'] for t in d.tweets]
        links += [{'source': node_names.index(t.status['text']),
                   'target': node_names.index('@'+m['screen_name']),
                   'type': 'mention'}
                  for d in data['users'] for t in d.tweets for m in t.status['entities']['user_mentions']]
        # connect the wildcard users
        links += [{'source': node_names.index(u1.username),
                   'target': node_names.index(u2.username),
                   'type': 'colleague'}
                  for u1 in data['users'] for u2 in data['users']]
        print(json.dumps({
            'nodes': nodes,
            'links': links,
        }))

if __name__ == '__main__':
    t = TwitterScraper()
    # t.scrape()
    # pprint([unicode(u) for u in t.load()['users']])
    data = t.load()
    t.filter_tweets(data)
    t.graph_json(data)
