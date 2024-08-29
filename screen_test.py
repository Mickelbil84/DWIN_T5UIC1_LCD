import time

# from RPi import GPIO
import LePotatoPi.GPIO.GPIO as GPIO

from icons import *
from screens import *
from encoder import Encoder
from DWIN_Screen import T5UIC1_LCD

LCD_COM_Port = '/dev/ttyAML6'

FPS = 5

def current_milli_time():
	return round(time.time() * 1000)

class ScreenTest(object):
    ENCODER_DIFF_NO = 0  # no state
    ENCODER_DIFF_CW = 1  # clockwise rotation
    ENCODER_DIFF_CCW = 2  # counterclockwise rotation
    ENCODER_DIFF_ENTER = 3   # click
    ENCODER_WAIT = 180
    ENCODER_WAIT_ENTER = 300
    EncoderRateLimit = True
         
    def __init__(self):
        self.lcd = T5UIC1_LCD(LCD_COM_Port)
        self.screen = Screen_MainMenu(self.lcd)

        self.encoder = Encoder(26, 19)
        self.EncodeLast = 0
        self.EncodeMS = current_milli_time() + self.ENCODER_WAIT
        self.EncodeEnter = current_milli_time() + self.ENCODER_WAIT_ENTER
        self.encoder.callback = self.encoder_callback

    def get_encoder_state(self):
        if self.EncoderRateLimit:
            if self.EncodeMS > current_milli_time():
                return self.ENCODER_DIFF_NO
            self.EncodeMS = current_milli_time() + self.ENCODER_WAIT

        if self.encoder.value < self.EncodeLast:
            self.EncodeLast = self.encoder.value
            return self.ENCODER_DIFF_CW
        elif self.encoder.value > self.EncodeLast:
            self.EncodeLast = self.encoder.value
            return self.ENCODER_DIFF_CCW
        # elif not GPIO.input(self.button_pin):
        #     if self.EncodeEnter > current_milli_time(): # prevent double clicks
        #         return self.ENCODER_DIFF_NO
        #     self.EncodeEnter = current_milli_time() + self.ENCODER_WAIT_ENTER
        #     return self.ENCODER_DIFF_ENTER
        else:
            return self.ENCODER_DIFF_NO
        
    def encoder_callback(self):
        state = self.get_encoder_state()
        if not self.screen.busy:
            self.screen.handle_input(state)

if __name__ == "__main__":
    ScreenTest()

    while True:
        pass