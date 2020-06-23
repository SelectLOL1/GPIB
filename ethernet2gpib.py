from __future__ import print_function, division
import socket


class Ethernet2GpibIf():
    def __init__(self, ip='10.10.32.223', gpibAddress=17):
        self.ip = ip
        self.port = 1234
        self.handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handle.connect((self.ip, self.port))
        self.setup(gpibAddress)

    def __del__(self):
        self.handle.close()

    def setup(self, gpibAddress):
        self.write('++addr {}'.format(gpibAddress))
        self.disableReadAfterWrite()
        self.setEndOfString2CRLF()
        self.setMode2Controller()
        self.enableEoi()

    def setGpibAddress(self, gpibAddress):
        self.write('++addr {}'.format(gpibAddress))
        self.disableReadAfterWrite()
        self.setEndOfString2CRLF()
        self.setMode2Controller()
        self.enableEoi()

    def enableReadAfterWrite(self):
        self.write('++auto 1')

    def disableReadAfterWrite(self):
        self.write('++auto 0')

    def setEndOfString2CRLF(self):
        self.write('++eos 0')

    def setMode2Controller(self):
        self.write('++mode 1')

    def enableEoi(self):
        self.write('++eoi 1')

    def write(self, command):
        self.handle.send(bytearray('{}\n'.format(command), 'ascii'))

    def ask(self, command):
        self.write(command)
        self.write('++read eoi')
        return self.read_response()

    def read_response(self):
        response = bytearray()
        part = self.handle.recv(4096)
        response += part
        return response

    def close(self):
        self.__del__()
