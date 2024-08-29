# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import time

#import RPi.GPIO as GPIO
import LePotatoPi.GPIO.GPIO as GPIO

from events import *

ROTARY_DEBOUNCE = 0.002

class RotaryInput:
    def __init__(self, left_pin, right_pin, button_pin):
        self.left_pin, self.right_pin, self.button_pin = left_pin, right_pin, button_pin

        GPIO.setup(self.left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.left_pin, GPIO.BOTH, callback=self.update_state)  
        GPIO.add_event_detect(self.right_pin, GPIO.BOTH, callback=self.update_state)  

        self.last_state = (GPIO.input(self.left_pin) << 1) | GPIO.input(self.right_pin)
        self.last_time = time.time()
        self.events = []
    
    def update_state(self):
        if time.time() - self.last_time < ROTARY_DEBOUNCE:
            return
        
        current_state = (GPIO.input(self.left_pin) << 1) | GPIO.input(self.right_pin)
        if current_state == self.last_state:
            return

        if (self.last_state == 0b00 and current_state == 0b01) or \
            (self.last_state == 0b01 and current_state == 0b11) or \
            (self.last_state == 0b11 and current_state == 0b10) or \
            (self.last_state == 0b10 and current_state == 0b00):
            self.events.append(EVENT_ROTARY_CCW)
        elif (self.last_state == 0b00 and current_state == 0b10) or \
            (self.last_state == 0b10 and current_state == 0b11) or \
            (self.last_state == 0b11 and current_state == 0b01) or \
            (self.last_state == 0b01 and current_state == 0b00):
            self.events.append(EVENT_ROTARY_CW)
        
        self.last_state = current_state
        self.last_time = time.time()

    def poll_event(self) -> int:
        if len(self.events) == 0:
            return EVENT_ROTARY_NONE
        
        # Cast majority vote on events
        cnts = {}
        for event in self.events:
            if event not in cnts:
                cnts[event] = 0
            cnts[event] += 1
        best_event = None
        best_cnt = -1
        for event, cnt in cnts.items():
            if cnt > best_cnt:
                best_cnt = cnt
                best_event = event

        self.events = []
        return best_event