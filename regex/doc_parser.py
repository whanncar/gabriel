
import re
import json
import os
import math


def extract_body_chunks(html):
	# Pull body from source
	body = re.findall("\[<a.*>.*</a>\]((?:.*\n*)*)</pre>", html)[0]
	# Get rid of lower bar
	body = re.split("__________", body)[0]
  # Gid rid of padding whitespace
	body = body.strip()
	# Pull chunks
	chunks = re.findall("((?:.+)(?:\n.+)*)\n\n+", body+"\n\n")
	# Clean up each chunk
	for i in range(len(chunks)):
		chunk = chunks[i]
		chunk = chunk.strip()
		# Kill annoying whitespace in chunks
		pars = re.split("\n ", chunk)
		for j in range(len(pars)):
			pars[j] = re.sub("\n", "", pars[j])
			pars[j] = pars[j].strip()
		chunk = ""
		for p in pars:
			chunk = chunk + p + "\n"
		chunks[i] = chunk.strip()
	return chunks


def clean_raw_text(filename):
	f = open(filename, 'r')
	html = f.read()
	f.close()
	chunks = extract_body_chunks(html)
	f = open(filename, 'w')
	f.write(json.dumps(chunks))
	f.close()



def clean_all_records(directory):
	files = os.listdir(directory)
	percent = 0
	num_files = len(files)
	for i in range(num_files):
		clean_raw_text(directory + "/" + files[i])
		new_percent = (i+1)/num_files
		new_percent = math.floor(new_percent)
		if new_percent > percent:
			percent = new_percent
			print str(percent) + "%\n"
