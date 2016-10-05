import gitlab
import time

from output import LCD

class Fetch:

	def __init__(self, private_token, project_id):
		self.private_token = private_token
		self.project_id = project_id
		self.client = gitlab.Gitlab('http://gitlab.com', self.private_token)
		self.lcd = LCD()

	def fetch_build_status(self):
		while (1):
			project = self.client.projects.get(self.project_id)
			if project is not None:
				latest_commit = self.client.project_commits.list(project_id=project.id, page=0, per_page=1)[0]
				latest_build = latest_commit.builds(page=0, per_page=1)[0];
				self.lcd.clear()
				self.lcd.message(project.path_with_namespace + ":\n" + latest_build.status)
			time.sleep(5)
