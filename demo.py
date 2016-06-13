import json, requests, datetime, ConfigParser, argparse, sys
from requests.auth import HTTPBasicAuth


def get_auth(whichAuth):
	file = 'python.properties'
	config = ConfigParser.RawConfigParser()
	config.read(file)
	token = config.get('ModeSection', 'token')
	password = config.get('ModeSection', 'password')
	auth = (token, password)
	return auth

def get_response_json(url, auth, isAuthNeeded):
	if(isAuthNeeded):
		response = requests.get(url, auth=auth)
	else:
		response = requests.get(url)
	return response.json()

def get_mode_results():

	if __name__ == '__main__':
		parser = argparse.ArgumentParser()
		parser.add_argument('-org', '--org')
		parser.add_argument('-reporttoken', '--reporttoken')
		parser.add_argument('-querytoken', '--querytoken')
		args = parser.parse_args()

	mode_url = 'https://modeanalytics.com'
	if(args.org is not None and args.reporttoken is not None):
		api_url = '/api/' + args.org + '/reports/' + args.reporttoken
	else:
		sys.exit('We did not get your -org or -report parameters.')

	auth = get_auth('mode')

	url = mode_url + api_url

	data = get_response_json(url, auth, True)

	links = data['_links']
	last_run = links['last_successful_run']
	run_url = last_run['href']	
	url = mode_url + run_url + '/query_runs/'

	data = get_response_json(url, auth, True)
	
	embedded = data['_embedded']
	query_runs = embedded['query_runs']
	#You need this part if there is more than one query in the report
	for x in query_runs:
		token = x['query_token']
		#print "Token: " + token
		if(token == args.querytoken):
			query_run = x['token']
	url = url + query_run + '/results'

	data = get_response_json(url, auth, True)

	links = data['_links']
	json = links['json']
	url = json['href']

	data = get_response_json(url, auth, False)

	i = 0

	for x in data:
		i = i + 1
		team = x['team']
		date = x['date']
		player = x['player']
		print str(i) + " " + date + " " + team + " " + player


get_mode_results()
