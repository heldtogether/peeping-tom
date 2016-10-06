import gitlab
import threading
import time

from output import LCD

class Fetch(threading.Thread):

	def __init__(self, should_exit, private_token, project_id):
		threading.Thread.__init__(self)
		self.should_exit = should_exit
		self.private_token = private_token
		self.project_id = project_id
		self.client = gitlab.Gitlab('http://gitlab.com', self.private_token)
		self.lcd = LCD()

	def run(self):
		while not self.should_exit.isSet():
			time.sleep(5)
			project = self.client.projects.get(self.project_id)
			if project is not None:
				latest_commit = self.client.project_commits.list(project_id=project.id, page=0, per_page=1)[0]
				latest_build = latest_commit.builds(page=0, per_page=1)[0];
				self.lcd.clear()
				self.lcd.message(project.path_with_namespace + ":\n" + latest_build.status)
