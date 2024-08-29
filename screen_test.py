import time

from DWIN_Screen import T5UIC1_LCD

LCD_COM_Port = '/dev/ttyAML6'

if __name__ == "__main__":
    lcd = T5UIC1_LCD(LCD_COM_Port)

    while True:
        # Get date time in format: "YYYY-MM-DD HH:MM:SS"
        date_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Clear screen
        lcd.Frame_Clear(lcd.Color_Bg_Black)
        lcd.Draw_String(True, False, lcd.font14x28, lcd.Color_White, 0, 10, 10, date_time)
        lcd.UpdateLCD()

        time.sleep(1 / 60)