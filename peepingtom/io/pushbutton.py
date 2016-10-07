import threading
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    from utils.mockgpio import GPIO


class PushButton(threading.Thread):
    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.daemon = True

        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        self.prev_input = None
        self.on_callback = None
        self.off_callback = None

    def set_on_callback(self, callback):
        self.on_callback = callback

    def set_off_callback(self, callback):
        self.off_callback = callback

    def run(self):
        while True:
            input = GPIO.input(self.pin)
            if not self.prev_input and input and self.on_callback:
                self.on_callback()
            elif self.prev_input and not input and self.off_callback:
                self.off_callback()
            self.prev_input = input
            time.sleep(0.1)
