
import json
import requests
import time
import csv

# This script checks the Hacker News top 30 stores (= frontpage) every minute and appends meta data
# for new entries into a .csv file for later analysis.

url_1st = ("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
top_1st = requests.get(url_1st)
top_1st.raise_for_status()
top_stories_1st = json.loads(top_1st.text)

starttime=time.time()

id_list = []


for id in top_stories_1st[0:30]:
    id_list.append(id)
time.sleep(60.0 - ((time.time() - starttime) % 60.0))

count = 1
hit_count = 0

while True:
    print("working #%s" % count)
    url = ("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
    top = requests.get(url)
    top.raise_for_status()
    top_stories = json.loads(top.text)
    for id in top_stories[0:30]:
        if id not in id_list:
            post = ("https://hacker-news.firebaseio.com/v0/item/%s.json?print=pretty" % id)
            item_post = requests.get(post)
            item_post.raise_for_status()
            hn_item = json.loads(item_post.text)
            title = hn_item.get('title', 0)
            score = hn_item.get('score', 0)
            post_time = hn_item.get('time', 0)
            user = hn_item.get('by', 0)
            now_time = int(time.time())
            time_dif = round((now_time - post_time)/60)
            id_list.append(id)
            with open('hn_entries.csv','a') as file:
                row = title + ";" + str(score) + ";" + str(post_time) + ";" + str(time_dif) + ";" + user + ";" + str(id) + "\n"
                file.write(row)
            hit_count += 1
            print("Number of recorded entries: %s" % hit_count)
    count += 1
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
