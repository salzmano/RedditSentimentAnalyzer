import praw
import pandas as pd
import numpy as np
import time

#Define Reddit connection
reddit = praw.Reddit(
    client_id = "mrqv6tH_ysUi3jB5wd5CvQ",
    client_secret = "LeHdHqWn8CPxgp_E9TCBTfhdiKJ-gQ",
    user_agent = "windows:rddtsentimentanalyzer:v1 (by /u/redsentana)"
)

#Define subreddit and Ticker
sub = reddit.subreddit("wallstreetbets")
ticker = "$GME"

#Define number of submissions and comments to inspect
sub_count = 5
cmt_count = 10

#Define submission list
sub_list = []
cmt_list = []

#Create pandas dataframe
#Cmt_ID - The comment ID can be used as key
#Sub_ID - Submission ID
#User - comment author
#Body - comment text
#Timestamp - time when comment was submitted
#Score - Upvote/Downvote ratio
df = pd.DataFrame(columns = ['Cmt_ID','Sub_ID','User','Body','Timestamp','Score'])
#Declare data list which we will fill with dictionary entries to later fill the dataframe
data_list = []

for idx, val in enumerate(sub.search("title:"+ticker, sort="top", time_filter="month", limit=sub_count)):
    print(val.title)
    print(idx)
    #get submission id
    sub_id = val.id
    sub_list.append(sub_id)

    submiss = reddit.submission(id=sub_id)

    #get top 100 top-level comments
    cmt_list.append(submiss.comments[:cmt_count])
    #remove stickied comments
    cmt_list[idx] = [i for i in cmt_list[idx] if i.stickied == False]
    #small test
    print(cmt_list[idx][0].body)

    #update dictionary
    for cmt in cmt_list[idx]:
        data_dict = {}
        # input values as described in the DataFrame
        #1 - Cmt_ID
        #2 - Sub_ID
        #3 - User
        #4 - Body
        #5 - Timestamp
        #6 - Score
        # key is the comment id

        #Do a check for deleted users
        if cmt.author is None:
            user = '[Deleted]'
        else:
            user = cmt.author.id

        data_dict.update({
            'Cmt_ID': cmt.id,
            'Sub_ID': sub_id,
            'User': user,
            'Body': cmt.body,
            'Timestamp': time.ctime(cmt.created_utc),
            'Score': cmt.score
        })
        data_list.append(data_dict)

#Fill DF
df = df.append(data_list)
df.head(5)

