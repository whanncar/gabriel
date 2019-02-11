
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
	json_response = get_response(url)
	dict_response = json.loads(json_response)
	return dict_response


# Give year as a string
def get_list_of_packages_by_year(year):
	packages = []
	page = 'https://api.govinfo.gov/collections/CREC/' + year + '-01-01T00:00:00Z?pageSize=100&offset=0'
	while page is not None:
		d = get_dict_response(page + '&api_key=' + api_key)
		for i in range(len(d['packages'])):
			if d['packages'][i]['packageId'].split('-')[1] == year:
				packages.append(d['packages'][i])
		page = d['nextPage']
	return packages
		


# p is a package in the sense of output from get_list_of_packages_by_year
def get_list_of_granules(p):
	granules = []
	package_summary = get_dict_response(p['packageLink'] + '?api_key=' + api_key)
	page = package_summary['granulesLink']
	while page is not None:
		d = get_dict_response(page + '&api_key=' + api_key)
		for i in range(len(d['granules'])):
			granules.append(d['granules'][i])
		page = d['nextPage']
	return granules


# g is a granule in the sense of output from get_list_of_granules
def get_granule_text(g):
	granule_summary = get_dict_response(g['granuleLink'] + '?api_key=' + api_key)
	text = get_response(granule_summary['download']['txtLink'] + '?api_key=' + api_key)
	return text


def save_list_of_packages(packages, folder):
	f = open(folder + '/templog.txt', 'w')
	f.write(json.dumps(packages))
	f.close()

def load_list_of_packages(folder):
	f = open(folder + '/templog.txt', 'r')
	packages = json.loads(f.read())
	f.close()
	return packages


def prepare_list_of_packages(year, folder):
	packages = get_list_of_packages_by_year(year)
	save_list_of_packages(packages, folder)


# Put everything together; year is a string; folder is where you want files stored
def get_congressional_record(folder):
	packages = load_list_of_packages(folder)
	############ For progress #########
	count = 0
	total = len(packages)
	###################################
	while len(packages) > 0:
		p = packages[0]
		print str(count) + '/' + str(total)
		count += 1
		success = True
		try:
			granules = get_list_of_granules(p)
			for g in granules:
				text = get_granule_text(g)
				name = g['granuleId'] + '.txt'
				f = open(folder + '/' + name, 'w')
				f.write(text)
				f.close()
		except:
			success = False
		if success:
			packages.pop(0)
		else:
			packages.append(packages.pop(0))
			count -= 1
		save_list_of_packages(packages, folder)


def revolve(folder):
	packages = load_list_of_packages(folder)
	back = packages.pop(0)
	packages.append(back)
	save_list_of_packages(packages, folder)



def instructions():
	print '\nfrom scraper import prepare_list_of_packages\nfrom scraper import get_congressional_record\nprepare_list_of_packages(year, folder)\nget_congressional_record(folder)'

# govinfo API docs: https://www.govinfo.gov/features/api
