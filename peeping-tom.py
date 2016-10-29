#!/usr/bin/python

import logging
import sys
import threading
import time

from peepingtom import Arguments, tasks, io


def main(argv):
    args = Arguments()
    args.parse_arguments(argv)

    logging.basicConfig(level=args.log_level)

    reset_button = io.PushButton(4)
    lcd = io.LCD()
    lcd_lock = threading.Lock()

    lcd_lock.acquire()
    lcd.message("Starting\nPeeping Tom...")
    time.sleep(2)
    lcd_lock.release()

    should_exit = threading.Event()
    setup = tasks.Setup(should_exit, args.debug, lcd, lcd_lock, reset_button)
    fetch = tasks.Fetch(should_exit, args.private_token, args.project_id, lcd, lcd_lock)

    fetch.start()
    setup.start()

    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        should_exit.set()


if __name__ == "__main__":
    main(sys.argv[1:])
