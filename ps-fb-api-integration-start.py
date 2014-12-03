import json, collections, facebook, urllib2

oauth_access_token = "CAACEdEose0cBAPHk5ZCsHWKqhGZA7VEBLxbEgIso69cHbIKQXiC0n58MTl0ORTuqlV1tJowxYWDnt0Gku331wYwpxp8hVsaGXLvp8yc3NGWV1qPzTc8jZCJMxZCnCp43EubjQv6ugdOf4K1hTd4qASzCUCtxvZAUjLUayisMFDcHX9ZCW1uRoDFjAfWYMAKIHWiPUE73VFMiM4YPxbjn9Y"
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

get_memes()