# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.
# Adapted from: https://github.com/nstansby/rpi-rotary-encoder-python/blob/master/encoder.py

import time

#import RPi.GPIO as GPIO
import LePotatoPi.GPIO.GPIO as GPIO

from events import *

ROTARY_DEBOUNCE = 0

class RotaryInput:
    def __init__(self, left_pin, right_pin, button_pin, beep_pin):
        self.left_pin, self.right_pin, self.button_pin, self.beep_pin = left_pin, right_pin, button_pin, beep_pin

        GPIO.setup(self.left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.beep_pin, GPIO.OUT)

        GPIO.add_event_detect(self.left_pin, GPIO.BOTH, callback=self.update_state)  
        GPIO.add_event_detect(self.right_pin, GPIO.BOTH, callback=self.update_state)  

        self.value = 0
        self.state = '00'
        self.direction = None
        self.events = []
        self.callback = None
    
    def update_state(self):        
        p1 = GPIO.input(self.left_pin)
        p2 = GPIO.input(self.right_pin)
        newState = "{}{}".format(p1, p2)
        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = "R"
            elif newState == "10": # Turned left 1
                self.direction = "L"

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Turned left 1
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.events.append(EVENT_ROTARY_CW if self.direction == "L" else EVENT_ROTARY_CCW)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = "L"
            elif newState == "00": # Turned right 1
                if self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.events.append(EVENT_ROTARY_CW if self.direction == "L" else EVENT_ROTARY_CCW)

        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.direction = "L"
            elif newState == "10": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.events.append(EVENT_ROTARY_CW if self.direction == "L" else EVENT_ROTARY_CCW)
                elif self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.events.append(EVENT_ROTARY_CW if self.direction == "L" else EVENT_ROTARY_CCW)
                
        self.state = newState
        
    def poll_event(self) -> int:
        if len(self.events) == 0:
            return EVENT_ROTARY_NONE
        
        e = self.events[-1]
        self.events = []
        return e
    
    def beep(self):
        GPIO.output(self.beep_pin, 1)
        time.sleep(0.1)
        GPIO.output(self.beep_pin, 0)