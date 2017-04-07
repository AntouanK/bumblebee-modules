# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

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
            bumblebee.output.Widget(full_text=self.price)
        )
        self._price = "-"
        self._interval = int(self.parameter("interval", "1"))
        self._nextcheck = 0
        self._valid = False

    def price(self, widget):
        if not self._valid:
            return u"?"
        return self._price

    def update(self, widgets):
        timestamp = int(time.time())
        if self._nextcheck < int(time.time()):
            try:
                self._nextcheck = int(time.time()) + self._interval*60
                price_url = "http://api.fixer.io/latest?symbols=USD,EUR&base=GBP" 
                price_json = json.loads( requests.get(price_url).text )
                gbpeur = str(price_json['rates']['EUR'])
                gbpusd = str(price_json['rates']['USD'])
                self._price = "£/€ " + gbpeur + " | £/$ " + gbpusd
                self._valid = True
            except RequestException:
                self._valid = False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

