import json, collections, facebook, urllib2

# replace token w new token
oauth_access_token = "CAACEdEose0cBAEZB6SNyyYCBwYyuDf4eKe14Lp88ZCHMTU8Q7mQCk559gmcNUCqksWdz2q67ygE0YvkwIbNvDDYs36QkyZC0Br3FRwHgTOLuAvjhpLUPAk3igMRrytjVtAVNO53E8mUF2dfuGK2I3ZAMuuYmqZAZACqydeRyZC1xcdcnsha8MwT2BNeIrBNEtYRfHiz0nSiCZCPi0pAZBhGc8"
graph = facebook.GraphAPI(oauth_access_token)

def get_memes():
	#get the graph
	# ps : 231149907051192
	# internet lonely : 1487896971464517
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
				try:
					excess = slurp(datum["likes"]["paging"]["next"])
					datum["comments"]["data"].extend(excess)
				except:
					print "keyerror?	", datum["comments"]["paging"]
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

def combine_memes():
	with open('0.json') as json_data:
		root = json.load(json_data)
		for i in xrange(1,17):
			name = "%d.json" % i
			with open(name) as lil_data:
				data = json.load(lil_data)
				root["data"].extend(data["data"])
		with open("internet_lonely_ULTIMATE.json", 'w') as save:
			save.write(json.dumps(root, sort_keys=True, indent=2))
#########################################################

get_memes()
combine_memes()
