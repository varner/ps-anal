import json
import collections
import xlwt

#making sure i open the json file safely
with open('ps_ULTIMATE.json') as data_file:
    # loading the json data
    data = json.load(data_file)
    postCount = len(data["data"])
    likeCount = 0
    mostLiked = 0
    commentCount = 0
    dates = []
    posters = []
    engagement = []
    # im iterating thru each post in the dataset
    for post in xrange(len(data["data"])): 
        datum = data["data"][post]
        #it's a dictionary so im just making sure the key is in the dictionary before accessing it
        if "likes" in datum:
            likeCount += len(datum["likes"]["data"])
            if (mostLiked < len(datum["likes"]["data"])):
                mostLiked = len(datum["likes"]["data"])
                mostLikedInfo = datum
        if "comments" in datum:
            commentCount += len(data["data"][post]["comments"]["data"])
        if "created_time" in datum:
            time_made = str(data["data"][post]["created_time"])[:10]
            dates.append(time_made)
        if "from" in datum:
            posters.append(datum["from"]["name"])

        if "from" in datum and "created_time" in datum and "id" in datum:
            if "likes" in datum:
                yay = len(datum["likes"]["data"])
            else:
                yay = 0
            engagement.append([datum["updated_time"], datum["from"]["name"], yay])

    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0,0,"Created Time")
    sheet1.write(0,1,"Posted By")
    sheet1.write(0,2,"Likes")
    for x in xrange(len(engagement)):
        print x
        sheet1.write(x+1,0, engagement[x][0])
        sheet1.write(x+1,1, engagement[x][1])
        sheet1.write(x+1,2, engagement[x][2])
    book.save("test.xls")
    print engagement[1]


    #aggregates total comments, likes, and posts for the json file
    print commentCount,"comments,", likeCount, "likes and", postCount, "posts ALL" 
    dates = sorted(dates)
    date_counter=collections.Counter(dates)
    poster_counter=collections.Counter(posters)
    # prints counts for amount of posts 
    print len(poster_counter), "people have ever posted to the group!"
    # prints the top posters in descending order
    print "Top Posters:"
    for letter, count in poster_counter.most_common(15):
        print '  %s: %d' % (letter, count)
    print# prints dates when the most posts were made in descending order
    print "Most Popular Days to Post:"
    for letter, count in date_counter.most_common(3):
        print '  %s: %d' % (letter, count)
    print
    #most liked post
    print mostLikedInfo["from"]["name"], "with", mostLiked,"likes, and here's the link:", mostLikedInfo["actions"]