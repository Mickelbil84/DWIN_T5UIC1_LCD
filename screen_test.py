import time

# from RPi import GPIO
import LePotatoPi.GPIO.GPIO as GPIO

from icons import *
from screens import *
from rotary_input import *
from encoder import Encoder
from DWIN_Screen import T5UIC1_LCD

LCD_COM_Port = '/dev/ttyAML6'
FPS = 60
ROTARY_DELAY = 0.1

def current_milli_time():
	return round(time.time() * 1000)

class ScreenTest(object):         
    def __init__(self):
        self.lcd = T5UIC1_LCD(LCD_COM_Port)
        self.screen = Screen_MainMenu(self.lcd)
        self.rotary = RotaryInput(26, 19 , 13, 6)
        # self.rotary.callback = self.rotary_callback
        self.rotary.beep()

        self.last_rotary_time = time.time()

    def handle_input(self, event):
        if time.time() - self.last_rotary_time < ROTARY_DELAY:
            return
        self.screen.handle_input(event)
        self.last_rotary_time = time.time()

    def run(self):
        while True:
            event = self.rotary.poll_event()
            if event >= 0:
                self.rotary.beep()
                print(event)
            self.handle_input(event)
            time.sleep(1 / FPS)

if __name__ == "__main__":
    screen_test = ScreenTest()
    screen_test.run()