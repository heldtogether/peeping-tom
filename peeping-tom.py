#!/usr/bin/python

import sys, getopt
import gitlab

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"ht:p:")
	except getopt.GetoptError:
		display_help()
		sys.exit(2)

	private_token = ''
	project_id = ''
	for opt, arg in opts:
		if opt == '-h':
			display_help()
			sys.exit()
		elif opt in ("-t"):
			private_token = arg
		elif opt in ("-p"):
			project_id = arg

	if private_token == '' or project_id == '':
		display_help()
		sys.exit(2)

	fetch_build_status(private_token, project_id)

def fetch_build_status(private_token, project_id):
	gl = gitlab.Gitlab('http://gitlab.com', private_token)

	latest_commit = gl.project_commits.list(project_id=project_id, page=0, per_page=1)[0]
	latest_build = latest_commit.builds(page=0, per_page=1)[0];

	print(latest_build.status)

def display_help():
	print 'peeping-tom.py -t <private-token> -p <project_id>'

if __name__ == "__main__":
   main(sys.argv[1:])
