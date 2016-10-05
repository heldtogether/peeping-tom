import gitlab
import time

class Fetch:

	def __init__(self, private_token, project_id):
		self.private_token = private_token
		self.project_id = project_id
		self.client = gitlab.Gitlab('http://gitlab.com', self.private_token)

	def fetch_build_status(self):
		while (1):
			latest_commit = self.client.project_commits.list(project_id=self.project_id, page=0, per_page=1)[0]
			latest_build = latest_commit.builds(page=0, per_page=1)[0];
			print(latest_build.status)
			time.sleep(5)
