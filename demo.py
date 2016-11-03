
import json, requests, datetime, ConfigParser, argparse, sys, yaml
from requests.auth import HTTPBasicAuth


def get_auth(whichAuth):
	with open ('mode.yml', 'r') as f:
		mode = yaml.load(f) 

	token = mode["mode"]["token"]
	password = mode["mode"]["password"]
	auth = (token, password)
	return auth

def get_response_json(url, auth):
	response = requests.get(url, auth=auth)
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
		sys.exit('We did not get your -org or -reporttoken parameters.')

	auth = get_auth('mode')

	url = mode_url + api_url

	print "API URL: " + url

	data = get_response_json(url, auth)

	links = data['_links']
	last_run = links['last_successful_run']
	run_url = last_run['href']	
	url = mode_url + run_url + '/query_runs/'

	data = get_response_json(url, auth)
	
	embedded = data['_embedded']
	query_runs = embedded['query_runs']
	#You need this part if there is more than one query in the report
	for x in query_runs:
		token = x['query_token']
		raw = x['raw_source']
		print "Query Token: " + token
		#print token + " SQL: \n" + raw
		print "*************************************"
		if(token == args.querytoken):
			query_run = x['token']

	if(args.querytoken is not None):
		url = url + query_run + '/results'
		print "Final URL: " + url
	else:
		sys.exit('We did not get your -querytoken parameter. Please choose a query token to use when running this code.')

	data = get_response_json(url, auth)

	links = data['_links']
	json = links['json']
	url = json['href']

	data = get_response_json(url, auth)

	i = 0

    #Change this to match the columns in your dataset as needed
	for x in data:
		i = i + 1
		team = x['team']
		date = x['date']
		player = x['player']
		print str(i) + " " + date + " " + team + " " + player


get_mode_results()

