
# Source: https://stackoverflow.com/questions/3949744/python-http-download-page-source

import urllib2
import json

api_key = 'AmT8pM8wtAJ9UAUNwtrg17EvcysVW0cnS8Zl5H8Q'



def get_response(url):

	# Set up header so that it doesn't reject requests
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
	headers = { 'User-Agent' : user_agent }

	# Get request ready
	req = urllib2.Request(url, None, headers)

	# Grab source code
	response = urllib2.urlopen(req)
	page = response.read()
	response.close()

  # Return source code string
	return page



def get_dict_response(url):
	url_with_key = url + '&api_key=' + api_key
	json_response = get_response(url_with_key)
	dict_response = json.loads(json_response)
	return dict_response



def get_list_of_2016_packages():
	packages = []
	page = 'https://api.govinfo.gov/collections/CREC/2016-01-01T00:00:00Z?pageSize=100&offset=0'
	while page is not None:
		d = get_dict_response(page)
		for i in range(len(d['packages'])):
			if d['packages'][i]['packageId'].split('-')[1] == '2016':
				packages.append(d['packages'][i])
		page = d['nextPage']
	return packages
		

# govinfo API docs: https://www.govinfo.gov/features/api
