
# Netdata plugin for dump1090-fa

[![Build Status](https://travis-ci.org/varnav/dump1090-netdata.svg?branch=devel)](https://travis-ci.org/varnav/dump1090-netdata) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/f62e5dde93e04d02a100d69ef9d9ca3a)](https://www.codacy.com/app/varnav/dump1090-netdata?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=varnav/dump1090-netdata&amp;utm_campaign=Badge_Grade)

## Installation

Copy `dump1090.chart.py` to `/usr/libexec/netdata/python.d/` and `dump1090.conf` to `/etc/netdata/python.d/`. Restart netdata `sudo systemctl restart netdata`.

In short:

```bash
git clone --depth 1 --branch devel https://github.com/varnav/dump1090-netdata.git
sudo cp dump1090-netdata/dump1090.chart.py /usr/libexec/netdata/python.d/
sudo cp dump1090-netdata/dump1090.conf /etc/netdata/python.d/
sudo cp dump1090-netdata/dump978.chart.py /usr/libexec/netdata/python.d/
sudo cp dump1090-netdata/dump978.conf /etc/netdata/python.d/
sudo systemctl restart netdata
```

[Netdata website](https://my-netdata.io/)
