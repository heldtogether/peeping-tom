import gitlab
import logging
import threading
import time


class Fetch(threading.Thread):
    def __init__(self, should_exit, private_token, project_id, lcd, lcd_lock):
        threading.Thread.__init__(self)
        self.should_exit = should_exit
        self.private_token = private_token
        self.project_id = project_id
        self.client = gitlab.Gitlab('http://gitlab.com', self.private_token)
        self.lcd = lcd
        self.lcd_lock = lcd_lock

    def run(self):
        while not self.should_exit.isSet():
            time.sleep(3)
            try:
                project = self.client.projects.get(self.project_id)
                if project is not None:
                    latest_commit = self.client.project_commits.list(project_id=project.id, page=0, per_page=1)[0]
                    latest_build = latest_commit.builds(page=0, per_page=1)[0];
                    self.lcd_lock.acquire()
                    self.lcd.clear()
                    self.lcd.message(project.path_with_namespace + ":\n" + latest_build.status)
                    time.sleep(2)
                    self.lcd_lock.release()
            except gitlab.GitlabConnectionError:
                logging.info("Could not connect to Gitlab.")
                self.lcd_lock.acquire()
                self.lcd.clear()
                self.lcd.message("Connection\nError :(")
                time.sleep(2)
                self.lcd_lock.release()
