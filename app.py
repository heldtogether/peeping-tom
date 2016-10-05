import getopt
import gitlab

class PeepingTom:

	def __init__(self, arguments):
		self.private_token = arguments.private_token
		self.project_id = arguments.project_id
		self.client = gitlab.Gitlab('http://gitlab.com', self.private_token)

	def fetch_build_status(self, project_id):
		latest_commit = self.client.project_commits.list(project_id=project_id, page=0, per_page=1)[0]
		latest_build = latest_commit.builds(page=0, per_page=1)[0];

		print(latest_build.status)

	def execute(self):
		self.fetch_build_status(self.project_id)


class PeepingTomArgs:

	def __init__(self):
		self.private_token = ''
		self.project_id = ''

	def parse_arguments(self, argv):
		try:
			opts, args = getopt.getopt(argv,"ht:p:")
		except getopt.GetoptError:
			self.display_help()
			sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				self.display_help()
				sys.exit()
			elif opt in ("-t"):
				self.private_token = arg
			elif opt in ("-p"):
				self.project_id = arg

		if self.private_token == '' or self.project_id == '':
			self.display_help()
			sys.exit(2)

	def display_help(self):
		print 'peeping-tom.py -t <private-token> -p <project_id>'
