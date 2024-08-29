import time

from icons import *
from events import *
from DWIN_Screen import T5UIC1_LCD
from screens.screen_base import Screen_Base, BUSY_DELAY

class Screen_MainMenu(Screen_Base):
    def __init__(self, lcd: T5UIC1_LCD):
        self.activeIcon = "print"
        self.icons = ["print", "prepare", "control", "info"]
        self.icon_callbacks = [self._icon_print, self._icon_prepare, self._icon_control, self._icon_info]

        Screen_Base.__init__(self, lcd, "Home")
    
    def init(self):
        self._icon_print()
        self._icon_prepare()
        self._icon_control()
        self._icon_info()

    def handle_input(self, event):
        if event == EVENT_ROTARY_CW:
            self._change_active_icon(1)
        elif event == EVENT_ROTARY_CCW:
            self._change_active_icon(-1)

    # d is +-1 (direction of change)
    def _change_active_icon(self, d: int):
        self.busy = True
        curr = self.icons.index(self.activeIcon)
        idx = curr + d
        if idx >= len(self.icons):
            idx = len(self.icons) - 1
        if idx < 0:
            idx = 0
        self.activeIcon = self.icons[idx]

        # Redraw only the two relevant icons
        self.icon_callbacks[curr]()
        self.icon_callbacks[idx]()
        self.refresh()
        
        time.sleep(BUSY_DELAY)
        self.busy = False

    # ------------------------------------------------------

    def _icon_print(self):
        if self.activeIcon == "print":
            self.lcd.ICON_Show(ICON_LIB, ICON_Print_1, 17, 130)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 17, 130, 126, 229)
            self.lcd.Frame_AreaCopy(1, 1, 451, 31, 463, 57, 201)
        else:
            self.lcd.ICON_Show(ICON_LIB, ICON_Print_0, 17, 130)
            self.lcd.Frame_AreaCopy(1, 1, 423, 31, 435, 57, 201)

    def _icon_prepare(self):
        if self.activeIcon == "prepare":
            self.lcd.ICON_Show(ICON_LIB, ICON_Prepare_1, 145, 130)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 145, 130, 254, 229)
            self.lcd.Frame_AreaCopy(1, 33, 451, 82, 466, 175, 201)
        else:
            self.lcd.ICON_Show(ICON_LIB, ICON_Prepare_0, 145, 130)
            self.lcd.Frame_AreaCopy(1, 33, 423, 82, 438, 175, 201)

    def _icon_control(self):
        if self.activeIcon == "control":
            self.lcd.ICON_Show(ICON_LIB, ICON_Control_1, 17, 246)            
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 17, 246, 126, 345)
            self.lcd.Frame_AreaCopy(1, 85, 451, 132, 463, 48, 318)
        else:
            self.lcd.ICON_Show(ICON_LIB, ICON_Control_0, 17, 246)
            self.lcd.Frame_AreaCopy(1, 85, 423, 132, 434, 48, 318)

    def _icon_leveling(self):
        if self.activeIcon == "leveling":
            self.lcd.ICON_Show(ICON_LIB, ICON_Leveling_1, 145, 246)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 145, 246, 254, 345)
            self.lcd.Frame_AreaCopy(1, 84, 437, 120, 449, 182, 318)
        else:
            self.lcd.ICON_Show(ICON_LIB, ICON_Leveling_0, 145, 246)
            self.lcd.Frame_AreaCopy(1, 84, 465, 120, 478, 182, 318)

    def _icon_info(self):
        if self.activeIcon == "info":
            self.lcd.ICON_Show(ICON_LIB, ICON_Info_1, 145, 246)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 145, 246, 254, 345)
            self.lcd.Frame_AreaCopy(1, 132, 451, 159, 466, 186, 318)
        else:
            self.lcd.ICON_Show(ICON_LIB, ICON_Info_0, 145, 246)
            self.lcd.Frame_AreaCopy(1, 132, 423, 159, 435, 186, 318)
