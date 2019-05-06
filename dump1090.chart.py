# -*- coding: utf-8 -*-
# Description: sump1090 log netdata python.d module
# Author: varnav
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from bases.FrameworkServices.UrlService import UrlService

# STATS_URL_978="http://localhost/skyview978"

ORDER = [
    'signals',
]

CHARTS = {
    'signals': {
        'options': [None, 'Signals', 'dB', 'statistics', 'apache.bytesperreq', 'line'],
        'lines': [
            ['signal', 'size', 'absolute', 1, 10],
            ['noise', 'size', 'absolute', 1, 10]
]}
}


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        #self.url1090 = self.configuration.get('url', 'http://localhost:8080/data/stats.json')
        self.url1090 = 'http://localhost:8080/data/stats.json'

    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        raw_data = self._get_raw_data()

        if not raw_data:
            return None

        data = dict()

        data = parse_line_local_float('signal', raw_data)
        data = parse_line_local_float('noise', raw_data)

        return data or None

def parse_line_local_float(label, line):
    
        #stats = json.load(urlopen(url1090, None, 5.0))
        stats = json.loads(line)
        data = dict()

        if stats['last1min'].has_key('local'):
            if stats['last1min']['local'].has_key(label):
                raw = stats['last1min']['local'][label]
                print("Boo!:", raw)
                # The current netdata API supports only integers, so multiply your float number by 100 or 1000 and set the divider of the dimension to the same number.
                data[label] = raw*10
        return data

