from serial import Serial
from random import random
from dataEmulator import Emulator

import numpy as np

import threading
import time

# List the possible baud rate.
baud_rate_list = [
    "75", "110", "300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"
]

class SerialPipe:
    """
    SerialPipe
    ==========
    Class that is used to interface the usb port.
    The call of the open function create a new thread that will read the 256 data frame formated as follow:
       (xxx,)*64
    The string is then converted into a numpy array and if it's 64 elements long the created array will be send to the callback
    If the array is not 64 element long the callback will be called with a False as argument. Letting user know that a frame has been droped.
    
    exemple
    -------

    def cb(data):
        print(data)

    ser = SerialPiep(cb)
    ser.port = "COMn"
    ser.open()
    ...
    ser.close()

    """

    def __init__(self, callback, debug=False):
        if debug:
            self.em = Emulator()
        self._serial = Serial()
        self._serial.timeout = 500
        self._port = ""
        self._baud_rate = 9600
        self.run = False
        self.callback = callback
        self.debug = debug

    def open(self):
        """
        Set the run flag to True has it is the one that handle while loop in the thread,
        open _serial and start the thread.
        """
        self.run = True
        if not self.debug:
            self._serial.open()
        t = threading.Thread(target=self.read_data)
        t.daemon = True
        t.start()

    def read_data(self):
        """
        If in debug mode update the emulator and pass his data to the callback function.
        If it is not in debug mode, 
        read the 256 long data frame to send it to the callback or send False in the callback 
        depending if data have been corrupted.
        """
        while self.run:
            if self.debug:
                data = self.em.update()
                self.callback(self.em.data)

                time.sleep(0.4)
            else:
                if self._serial.in_waiting >= 256:
                    data = self._serial.read_until()
                    data_array = np.fromstring(data, sep=',', dtype=int)
                    if len(data_array) == 64:
                        self.callback(data_array)
                    else:
                        self.callback(False)
                time.sleep(0.01)

    def close(self):
        """
        Reset the run flag to close the read_data thread and close the USB port.
        """
        self.run = False
        if not self.debug:
            self._serial.close()

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