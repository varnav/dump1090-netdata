#!/usr/bin/env python2

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

update_every = 1
priority = 60000
retries = 10

ORDER = [
    'signals',
]

CHARTS = {
    'signals': {
        'options': [None, 'Signals', 'dB', 'statistics', 'apache.bytesperreq', 'line'],
        'lines': [
            ['signal', 'power', 'absolute', 1, 10],
            ['noise', 'power', 'absolute', 1, 10]
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

        data["signal"] = parse_line_local_float('signal', raw_data)
        data["noise"] = parse_line_local_float('noise', raw_data)

        return data or None

def parse_line_local_float(label, line):
    
        #stats = json.load(urlopen(url1090, None, 5.0))
        stats = json.loads(line)

        if stats['last1min'].has_key('local'):
            if stats['last1min']['local'].has_key(label):
                raw = stats['last1min']['local'][label]
                # The current netdata API supports only integers, so multiply your float number by 100 or 1000 and set the divider of the dimension to the same number.
                data = raw*10
        return data

