#!/usr/bin/env python

"""
The MIT License (MIT)
Copyright (c) 2016-2017 Jan Arnold
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# @Title            : dump1090.chart
# @Description      : NetData plugin for dump1090
# @Author           : Evgeny Varnavskiy
# @Email            : varnavruz@gmail.com
# @Copyright        : Evgeny Varnavskiy
# @License          : MIT
# @Maintainer       : Evgeny Varnavskiy
# @Date             : 2019/05/06
# @Version          : 0.1
# @Notes            : With default NetData installation put this file under
#                   : /usr/libexec/netdata/python.d/ and the config file under
#                   : /etc/netdata/python.d/
"""

import json
from bases.FrameworkServices.UrlService import UrlService

update_every = 20
priority = 60000
retries = 10

ORDER = [
    'messages',
    'signals',
    'strong_signals',
    'samples'
]

CHARTS = {
    'signals': {
        'options': [None, 'Signals last 1m', 'dB', 'signals', 'signals', 'line'],
        'lines': [
            ['signal', 'power', 'absolute', 1, 10],
            ['noise', 'noise', 'absolute', 1, 10],
            ['peak_signal', 'peak_signal', 'absolute', 1, 10],
]},

    'strong_signals': {
        'options': [None, 'Strong signals last 1m', 'N', 'signals', 'signals', 'line'],
        'lines': [
            ['strong_signals', 'strong_signals', 'absolute']
]},

    'messages': {
        'options': [None, 'Messages last 1m', 'N', 'messages', 'messages', 'area'],
        'lines': [
            ['messages', 'messages', 'absolute']
]},

    'samples': {
        'options': [None, 'Samples last 1m', 'N', 'samples', 'samples', 'area'],
        'lines': [
            ['samples_processed', 'Processed', 'absolute'],
            ['samples_dropped', 'Dropped', 'absolute'],
            ['modeac', 'Mode A/C', 'absolute'],
            ['modes', 'Mode S', 'absolute'],
]}

}




class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.url1090 = self.configuration.get('url', 'http://localhost:8080/data/stats.json')
        #self.url1090 = 'http://localhost:8080/data/stats.json'

    def check(self):
        self._manager = self._build_manager()

        data = self._get_data()

        if not data:
            return None

        return True

    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        raw_data = self._get_raw_data()

        data = dict()

        if not raw_data:
            return None

        data["signal"] = parse('last1min','local','signal', raw_data, 1)
        data["noise"] = parse('last1min','local','noise', raw_data, 1)
        data["peak_signal"] = parse('last1min','local','peak_signal', raw_data, 1)
        data["strong_signals"] = parse('last1min','local','strong_signals', raw_data, 0)
        data["messages"] = parse('last1min','messages', 0, raw_data, 0)
        data["samples_processed"] = parse('last1min', 'local', 'samples_processed', raw_data, 0)
        data["samples_dropped"] = parse('last1min', 'local', 'samples_dropped', raw_data, 0)
        data["modeac"] = parse('last1min', 'local', 'modeac', raw_data, 0)
        data["modes"] = parse('last1min', 'local', 'modes', raw_data, 0)

        return data or None

def parse(l1, l2, l3, rawjson, fl=bool):
    
    stats = json.loads(rawjson)

    raw = float()
    res = int()

    if stats[l1].has_key(l2):
        if (l3 == 0):
            raw = stats[l1][l2]
        elif stats[l1][l2].has_key(l3):
            raw = stats[l1][l2][l3]
            # The current netdata API supports only integers, so multiply your float number by 100 or 1000 and set the divider of the dimension to the same number.
            #print(raw, type(raw))
        if fl:
            res = raw*10
        else:
            res = raw

        return res
