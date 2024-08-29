import time

from icons import *
from DWIN_Screen import T5UIC1_LCD

LCD_COM_Port = '/dev/ttyAML6'

FPS = 30

if __name__ == "__main__":
    lcd = T5UIC1_LCD(LCD_COM_Port)

    frame = 0
    icon_id = 0
    while True:
        # Get date time in format: "YYYY-MM-DD HH:MM:SS"
        date_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Clear screen
        lcd.Frame_Clear(lcd.Color_Bg_Black)
        lcd.Draw_String(True, False, lcd.font14x28, lcd.Color_White, 0, 10, 10, date_time)
        lcd.ICON_Show(ICON_LIB, icon_id, 10, 50)
        lcd.UpdateLCD()

        frame += 1
        if frame >= 60 / 4:
            frame = 0
            icon_id += 1
            if icon_id > 91:
                icon_id = 0

        time.sleep(1 / FPS)