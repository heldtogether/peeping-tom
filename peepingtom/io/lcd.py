try:
    from Adafruit_CharLCD import Adafruit_CharLCD
except ImportError:
    import utils.mocklcd as Adafruit_CharLCD

# Raspberry Pi pin configuration:
lcd_rs = 27
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2


class LCD(Adafruit_CharLCD.Adafruit_CharLCD):
    def __init__(self):
        Adafruit_CharLCD.Adafruit_CharLCD.__init__(self, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns,
                                                   lcd_rows, lcd_backlight)
