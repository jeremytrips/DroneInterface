from serial import Serial
from random import random
from dataEmulator import Emulator

import numpy as np

import threading
import time

baud_rate_list = [
    "75", "110", "300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"
]

OPEN_COM_CHAR = 0x01010101
END_TRAN_CHAR = '%'
END_COM_CHAR = 0x11111110

class SerialPipe:

    def __init__(self, callback, debug=False):
        if debug:
            self.em = Emulator()
        self._serial = Serial()
        self._serial.timeout = 500
        self._port = ""
        self._baud_rate = 9600
        self.run = True
        self.callback = callback
        self.debug = debug

    def open(self):
        print("opening")
        self.run = True
        t = threading.Thread(target=self.read_data)
        t.daemon = True
        t.start()
        if not self.debug:
            self._serial.open()

    def read_data(self):
        while self.run:
            if self.debug:
                data = self.em.update()
                self.callback(self.em.data, self.em.hot_point_coordinate)

                time.sleep(0.4)
            else:
                if self._serial.in_waiting >= 256:
                    data = self._serial.read_until()
                    data_array = np.fromstring(data, sep=',', dtype=int)
                    print(data)
                    if len(data_array) == 64:
                        self.callback(data_array)
                else:
                    self.callback(False)
                time.sleep(0.01)

    def close(self):
        print("closing")
        self.run = False
        if not self.debug:
            self._serial.close()
            self._serial.write

    @property
    def is_open(self):
        return self._serial.is_open

    @property
    def can_open(self):
        if self.debug:
            return True
        return self._serial.port != None

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
        self._serial.port = value

    @property
    def baud_rate(self):
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, value):
        self._baud_rate = value


if __name__ == "__main__":
    def test(a, b):
        print(a)
    a = SerialPipe(test)
    a.port = "COM11"
    a.open()