from icons import *
from DWIN_Screen import T5UIC1_LCD

BUSY_DELAY = 0.01

class Screen_Base(object):
    def __init__(self, lcd: T5UIC1_LCD, title: str):
        self.lcd = lcd
        self.lcd.JPG_CacheTo1(1)
        self.lcd.Frame_Clear(self.lcd.Color_Bg_Black)
        self._title_bar(title)
        self._icon_logo()

        # Overriden by polymorphism
        self.init()

        self.refresh()
        self.busy = False

    def init(self):
        pass

    def handle_input(self, state):
        pass

    def refresh(self):
        self.lcd.UpdateLCD()

    def _icon_logo(self):
        self.lcd.ICON_Show(ICON_LIB, ICON_LOGO, 71, 52)

    def _title_bar(self, title: str):
        self.lcd.Draw_Rectangle(1, self.lcd.Color_Bg_Blue, 0, 0, self.lcd.DWIN_WIDTH, 30)
        self.lcd.Draw_String(False, False, self.lcd.font10x20, self.lcd.Color_White, 0, 10, 7, title)