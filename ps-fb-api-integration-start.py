import json
import collections
import facebook

oauth_access_token = "whatever"
graph = facebook.GraphAPI(oauth_access_token)
#profile = graph.get_object("me")
#friends = graph.get_connections("me", "friends")
#graph.put_object("me", "feed", message="I am writing on my wall!")

def test():
	with open('ps.json') as data_file:
		data = json.load(data_file)
		postCount = len(data["data"])
		likeCount = 0
		commentCount = 0
		dates = []
		posters = []
	
		for i in xrange(len(data["data"])):
			datum = data["data"][i]
			if "likes" in datum:
				likeCount += len(datum["likes"]["data"])
			if "comments" in datum:
				commentCount += len(data["data"][i]["comments"]["data"])
			if "created_time" in datum:
				time_made = str(data["data"][i]["created_time"])[:10]
				dates.append(time_made)
			if "from" in datum:
				posters.append(datum["from"]["name"])
	
		print commentCount,"comments,", likeCount, "likes and", postCount, "posts since Oct 7 2014" 
		dates = sorted(dates)
		date_counter=collections.Counter(dates)
		poster_counter=collections.Counter(posters)
		print len(poster_counter)
		print poster_counter
		print date_counter