from kivy.app import App

from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.core.audio import SoundLoader

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

from kivy.uix.spinner import Spinner

from serial.tools import list_ports 

import time
import threading
import numpy as np
from random import random

from serial_pipe import SerialPipe, baud_rate_list


class SerialLayout(BoxLayout, Widget):
    com_state = StringProperty("Not connected")
    button_text = StringProperty("Connect")
    com_selected = StringProperty("")
    com_available = ListProperty([])
    baud_rate_available = ListProperty(baud_rate_list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        threading.Thread(target=self.fetch_available_com_port).start()

    def fetch_available_com_port(self):
        ports = list_ports.comports()
        for port in ports:
            self.com_available.append(port.name)

    def set_com_selected(self, selected):
        self.com_selected = selected

class Pixel(Widget):
    color = ListProperty([0.8,0.8,0.8,1])

    def set_color(self, color):
        self.color = color, color, color, 1


class CameraRenderingLayout(GridLayout, Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainLayout(BoxLayout):
    pass

def twoCompl12(val):
    if  0x7FF & val == val:
        return float(val)
    else:
        return float(val-4096 )


class MainApp(App):
    serial_layout = None
    pixels_layout = None
    average_temp = StringProperty(-1)
    frame_drop = NumericProperty(0)
    alert_temp = NumericProperty(30)    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected = False
        self.pixels = []
        self.pipe = SerialPipe(self.update, True)
        self.alert_sound = SoundLoader.load("alert.wav")
        self.alert_mode = False

    def on_start(self):
        self.serial_layout = self.root.ids["serial_layout"]
        self.pixels_layout = self.root.ids["pixels_layout"]
        for i in range(64):
            tmp = Pixel()
            self.pixels.append(tmp)
            self.pixels_layout.add_widget(tmp)

    def on_stop(self):
        self.pipe.run = False

    def update(self, data):
        if data is False:
            self.frame_drop += 1
            return 
        data = data/255
        tmp = round(np.average(data), 2)
        self.average_temp = str(tmp)
        if tmp >= self.alert_temp:
            self.alert_thread()
        for i in range(64):
            self.pixels[i].set_color(data[i])

    def alert_thread(self):
        if not self.alert_mode:
            self.alert_mode = True
            threading.Thread(target=self._alert_thread).start()

    def _alert_thread(self, n=10):
        for i in range(n):
            self.alert_sound.play()
            time.sleep(1)
        self.alert_mode = False        

    def set_com_selected(self, com):
        self.pipe.port = com

    def set_baud_rate(self, value):
        self.pipe.baud_rate = value

    def connect_com_port(self):
        if self.pipe.can_open:     
            self.pipe.open()
            self.serial_layout.button_text = "Disconnect"
            self.serial_layout.com_state = "Connected"
            self.connected = True
    
    def disconnect_com_port(self):
        self.pipe.close()
        self.connected = False
        self.serial_layout.button_text = "Connect"
        self.serial_layout.com_state = "Not Connected"
    
    def on_stop(self):
        self.disconnect_com_port()

    def __del__(self):
        self.pipe.run = False

if __name__ == "__main__":
    MainApp().run()
