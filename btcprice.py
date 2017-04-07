# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays the temperature on the current location based on the ip
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import json
import time
try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.btcprice)
        )
        self._interval = int(self.parameter("interval", "1"))
        self._nextcheck = 0
        self._valid = False

    def update(self, widgets):
        timestamp = int(time.time())
        if self._nextcheck < int(time.time()):
            try:
                self._nextcheck = int(time.time()) + self._interval*60
                btcprice_url = "curl -s http://api.coindesk.com/v1/bpi/currentprice.json | grep -oE EUR.+ | pcregrep -o1 'rate\":\"(.+?)\"'"
                btcprice = json.loads(requests.get(btcprice_url).text)
                self._valid = True
            except RequestException:
                self._valid = False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

