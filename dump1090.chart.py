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

UPDATE_EVERY = 20
PRIORITY = 60000
RETRIES = 10

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

    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        raw_data = self._get_raw_data()

        data = dict()

        if not raw_data:
            return None

        data["signal"] = parse('last1min', 'local', 'signal', raw_data, True)
        data["noise"] = parse('last1min', 'local', 'noise', raw_data, True)
        data["peak_signal"] = parse('last1min', 'local', 'peak_signal', raw_data, True)
        data["strong_signals"] = parse('last1min', 'local', 'strong_signals', raw_data, False)
        data["messages"] = parse('last1min', 'messages', '', raw_data, False)
        data["samples_processed"] = parse('last1min', 'local', 'samples_processed', raw_data, False)
        data["samples_dropped"] = parse('last1min', 'local', 'samples_dropped', raw_data, False)
        data["modeac"] = parse('last1min', 'local', 'modeac', raw_data, False)
        data["modes"] = parse('last1min', 'local', 'modes', raw_data, False)

        return data or None


def parse(l1, l2, l3, rawjson, fl):
    """Parse JSON stats from dump1090

    Args:
        l1 (str): Level 1 name of JSON tree
        l2 (str): Level 2 name of JSON tree
        l3 (str): Level 3 name of JSON tree
        rawjson (str): JSON to parse
        param2 (bool): Is this a float type data?

    Returns:
        int: Value of given stat

    """

    stats = json.loads(rawjson)

    raw = float()

    if l2 in stats[l1]:
        if not l3:
            raw = stats[l1][l2]
        elif l3 in stats[l1][l2]:
            raw = stats[l1][l2][l3]
            # The current netdata API supports only integers, so multiply your float number by
            # 100 or 1000 and set the divider of the dimension to the same number.
        
    if fl:
        res = raw * 10
    else:
        res = raw

    return res or None
