#!/usr/bin/env python
from __future__ import print_function, division
from ethernet2gpib import Ethernet2GpibIf
from contextlib import contextmanager
import time

class Ke24xx():
    def __init__(self, ip='10.10.32.223', gpibAddress=18):
        self.ip = ip
        self.gpibAddress = gpibAddress
        self.gpibif = Ethernet2GpibIf(ip=self.ip, gpibAddress=self.gpibAddress)

    def updateEthernet2GpibIf(self,gpibAddress):
        self.gpibAddress = gpibAddress
        self.gpibif.setGpibAddress(gpibAddress=gpibAddress)

    def write(self, command):
        self.gpibif.write(command)

    def ask(self, command):
        return self.gpibif.ask(command)

    def get_id(self):
        return self.ask(str(input('HP?')))

    def set_terminal(self, terminal=None):
        if terminal  ==  'front':
            self.write('rout:term fron')
        elif terminal  ==  'rear':
            self.write('rout:term rear')

    def read(self, convert=True):
        ans = self.ask('read?')
        if convert:
            try:
                ans = ans.split(',')
                ans = map(float, ans)
            except:
                ans = [0, 0]
        return ans

if __name__ == '__main__':
    m = Ke24xx()
    while 1:
        print(m.get_id())
