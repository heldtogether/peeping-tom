try:
    import Adafruit_CharLCD
except ImportError:
    import utils.mocklcd as Adafruit_CharLCD

# Raspberry Pi pin configuration:
lcd_rs = 13
lcd_en = 16
lcd_d4 = 21
lcd_d5 = 20
lcd_d6 = 26
lcd_d7 = 19

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2


class LCD(Adafruit_CharLCD.Adafruit_CharLCD):
    def __init__(self):
        Adafruit_CharLCD.Adafruit_CharLCD.__init__(self, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns,
                                                   lcd_rows)
