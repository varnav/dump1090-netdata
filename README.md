# Netdata plugin for dump1090-fa
[![Build Status](https://travis-ci.org/varnav/dump1090-netdata.svg?branch=devel)](https://travis-ci.org/varnav/dump1090-netdata)

## Installation

Copy to `dump1090.chart.py` to `/usr/libexec/netdata/python.d/` and `dump1090.conf` to `/etc/netdata/python.d/`. Restart netdata `sudo systemctl restart netdata`.

In short:

```
git clone --depth 1 --branch devel https://github.com/varnav/dump1090-netdata.git
sudo cp dump1090-netdata/dump1090.chart.py /usr/libexec/netdata/python.d/
sudo cp dump1090-netdata/dump1090.conf /etc/netdata/python.d/
systemctl restart netdata
```

[Netdata website](https://my-netdata.io/)
