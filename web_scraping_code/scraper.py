
# Source: https://stackoverflow.com/questions/3949744/python-http-download-page-source

import urllib2


def get_source_code(url):

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
