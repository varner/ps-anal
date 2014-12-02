import json, collections, facebook, urllib2

oauth_access_token = "CAACEdEose0cBACrEr6KCESRjKGZBKSwp9F5aujoQlb9s7YFGi91698vFLgUMdi5ZCcKwFmUm6cCz9lv0lZBC2ZBySzHrVfiMoODUcgRuPaJRQOMcZAwhCWzo7NFoMJYL9HbSRxZBHeMeiy6ZBHyL1T7bU9B2pwQU6WpnNafRn91ZCUmem7ZAot6RhVO3ZAfJOXYWO8P019I5wNbeJMGI7niors"
graph = facebook.GraphAPI(oauth_access_token)

def get_memes():
	#get the graph
	group = graph.get_object("231149907051192/feed", limit=999)
	current = group
	iteration = 0
	while current != False:
		saveName = "%d.json" % iteration
		download_memes(current, saveName)
		if "paging" in current and "next" in current["paging"]:
			url = current["paging"]["next"]
			page = urllib2.urlopen(url)
			next = json.load(page)
		else:
			next = False
		iteration += 1
		current = next


def download_memes(data, saveName):
	print type(data)
	#ok now expand all comment/like data ^______^
	for post in xrange(len(data["data"])): 
		datum = data["data"][post]
		#it's a dictionary so im just making sure the key is in the dictionary before accessing it
		if "likes" in datum:
			if "next" in datum["likes"]["paging"]:
				try:
					excess = slurp(datum["likes"]["paging"]["next"])
					datum["likes"]["data"].extend(excess)
				except:
					print "keyerror?	", datum["likes"]["paging"]
		if "comments" in datum:
			if "next" in datum["comments"]["paging"]:
				excess = slurp(datum["likes"]["paging"]["next"])
				datum["comments"]["data"].extend(excess)
	#SAVE IT ALLLLL TO A SINGLE FILE LMFAO 
	with open(saveName, 'w') as save:
		save.write(json.dumps(data, sort_keys=True, indent=2))

#this crawls thru next links and then merges all the data
def slurp(next):
	response = urllib2.urlopen(next)
	data = json.load(response)
	laterData     = []
	currentData   = []
	if "data" in data:
		currentData = data["data"]
		if "paging" in data and "next" in data["paging"]:
			laterData = slurp(data["paging"]["next"])
	if laterData != None and currentData != None:
		currentData.extend(laterData)
	return currentData

get_memes()