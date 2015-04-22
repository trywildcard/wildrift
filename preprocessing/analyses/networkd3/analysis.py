"""Networkd3 analysis. Just a placeholder."""

import databench

import pickle
from pprint import pprint
from twitterscraper import TwitterScraper, User, Tweet


class Analysis(databench.Analysis):

    def on_connect(self):
        """Run as soon as a browser connects to this."""
        self.emit('log', 'backend is connected and initialized')

        # t = TwitterScraper()
        # t.scrape()
        # pprint([unicode(u) for u in t.load()['users']])

        self.emit('graph', {
            'nodes': [
                {'name': 'trywildcard'},
                {'name': 'jordancooper'},
                {'name': 'petkanics'},
                {'name': 'ericxtang'},
            ],
            'links': [
                {'source': 0, 'target': 1, 'type': 'follow'},
                {'source': 0, 'target': 2, 'type': 'follow'},
                {'source': 0, 'target': 3, 'type': 'follow'},
            ]
        })


META = databench.Meta('networkd3', __name__, __doc__, Analysis)
