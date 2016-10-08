import sys


class Adafruit_CharLCD:
    def __init__(self, rs, en, d4, d5, d6, d7, cols, lines, backlight=None,
                 invert_polarity=True,
                 enable_pwm=False,
                 gpio=None,
                 pwm=None,
                 initial_backlight=1.0):
        pass

    def home(self):
        pass

    def clear(self):
        pass

    def set_cursor(self, col, row):
        pass

    def enable_display(self, enable):
        pass

    def show_cursor(self, show):
        pass

    def blink(self, blink):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def set_left_to_right(self):
        pass

    def set_right_to_left(self):
        pass

    def autoscroll(self, autoscroll):
        pass

    def message(self, text):
        print(text)

    def set_backlight(self, backlight):
        pass

    def write8(self, value, char_mode=False):
        pass

    def create_char(self, location, pattern):
        pass
