
def get_congressperson_names(text):
	return re.findall("(?:Ms\.|Mrs\.|Mr\.) ([A-Z][\-a-zA-Z]*[A-Z])[^a-zA-Z]", text)


