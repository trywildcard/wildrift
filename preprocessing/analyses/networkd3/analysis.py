"""Networkd3 analysis. Just a placeholder."""

import databench

import json
# import pickle
from pprint import pprint
# from twitterscraper import TwitterScraper


class Analysis(databench.Analysis):

    def on_connect(self):
        """Run as soon as a browser connects to this."""
        self.emit('log', 'backend is connected and initialized')

        # self.emit('graph', {
        #     'nodes': [
        #         {'name': '@trywildcard'},
        #         {'name': '@jordancooper'},
        #         {'name': '@petkanics'},
        #         {'name': '@ericxtang'},
        #     ],
        #     'links': [
        #         {'source': 0, 'target': 1, 'type': 'follow'},
        #         {'source': 0, 'target': 2, 'type': 'follow'},
        #         {'source': 0, 'target': 3, 'type': 'follow'},
        #     ]
        # })

        # t = TwitterScraper()
        # t.scrape()
        # pprint([unicode(u) for u in t.load()['users']])

        with open('graph.json', 'rb') as f:
            d = json.load(f)
            self.emit('graph', d)



META = databench.Meta('networkd3', __name__, __doc__, Analysis)
