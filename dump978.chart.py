#!/usr/bin/env python

"""
The MIT License (MIT)
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
# @Title            : dump978.chart
# @Description      : NetData plugin for dump978
# @Author           : Evgeny Varnavskiy
# @Email            : varnavruz@gmail.com
# @Copyright        : Evgeny Varnavskiy
# @License          : MIT
# @Maintainer       : Evgeny Varnavskiy
# @Date             : 2019/05/08
# @Version          : 0.1
# @Notes            : With default NetData installation put this file under
#                   : /usr/libexec/netdata/python.d/ and the config file under
#                   : /etc/netdata/python.d/
"""

import json
from bases.FrameworkServices.UrlService import UrlService # pylint: disable=E0401, E0611

UPDATE_EVERY = 10
PRIORITY = 60000
RETRIES = 10

ORDER = [
    'messages',
    'aircraft'
]

CHARTS = {
    'messages': {
        'options': [None, 'Messages total', 'N', 'messages', 'messages', 'area'],
        'lines': [
            ['messages', 'messages', 'absolute']
        ]},

    'aircraft': {
        'options': [None, 'Aircraft tracked now', 'N', 'aircraft', 'aircraft', 'area'],
        'lines': [
            ['tracked_now', 'N', 'absolute']
        ]}

}


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.url = self.configuration.get('url', 'http://localhost:8978/data/stats.json')

    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        raw_data = self._get_raw_data()

        data = dict()

        if not raw_data:
            return None

        stats = json.loads(raw_data)

        # We multiple float values by 10 there and set delimeter to 10 in charts definition
        # It's the only way to get float values in Netdata for now
        data["messages"] = parse('aircraft', 'messages', '', stats)
        data["tracked_now"] = len(stats['aircraft'])

        return data or None


def parse(l1, l2, l3, stats):
    """Parse JSON stats from dump978

    Args:
        l1 (str): Level 1 name of JSON tree
        l2 (str): Level 2 name of JSON tree
        l3 (str): Level 3 name of JSON tree
        stats (str): JSON to parse

    Returns:
        int: Value of given stat

    """

    raw = int()

    if l2 in stats[l1]:
        if not l3:
            raw = stats[l1][l2]
        elif l3 in stats[l1][l2]:
            raw = stats[l1][l2][l3]
            # The current netdata API supports only integers, so multiply your float number by
            # 100 or 1000 and set the divider of the dimension to the same number.
    return raw or None
