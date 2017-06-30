import json
import requests
import pprint
import time
import matplotlib.pyplot as plt
from matplotlib import style


# This script accesses the newest contributions to Hacker News, tracks the number of upvotes, saves them to text files
# and plots them right away (if indicated), frequently updated.
# I had problems with using Matplot's interactive mode (ION()) and the .draw() command.
# Therefore I rely on the .show() command every 3 minutes and force it to close after 60 seconds. It's not
# ideal because it keeps popping up into the foreground every time it loads.
# I might find a solution for it later.
# HN API Doc https://github.com/HackerNews/API/blob/master/README.md'''


# file-to_list function prepares the tracked scores for the lists used for plotting

def file_to_list(file,number,title,id,score):
    list = []
    with open(file, "a") as file_scores:
        if counter_dict[number] == 0:
            first_line = ("%s , %s" % (title,id))
            pprint.pprint(first_line, file_scores)
            major_list.append([])
            major_list[number-1].append(title)
            counter_dict[number] += 1
        pprint.pprint(score, file_scores)
        major_list[number-1].append(score)

# plot function handles the plotting and the automatic closing of the plot

def plot():
    timestamp = []
    for item in range(len(major_list[0])):
        timestamp.append(item)

    style.use('fivethirtyeight')

    font = {'family' : 'arial',
            'weight' : 'light',
            'size'   : 8}

    plt.rc('font', **font)

    for index in range(items_tracked):
        plt.plot(timestamp[0:-1],major_list[index][1:], label=major_list[index][0])

    plt.xlabel('time (in minutes)')
    plt.ylabel('Score')
    plt.title('Scores over time for selected Hacker News articles')
    plt.legend()
    plt.ylim(ymin=0) # remove if y-axis should not be forced to start at 0.
    plt.show(block = False)


items_tracked = 10 #adjust here how many items from the 'new' section should be tracked (descending).

user_input_plot = input("Do you want to plot 'live'? Type 'y'. Any other key will only save scores to txt files: ")
print("Thank you. Accessing the data...")

# counter dict generates counters for each item stored in a dict, to be used in order to access
# the Hacker News post's title only once during the processing.


major_list = [] # will store lists with the scores for each item.

starttime=time.time()
count_for_plotting = 0


# accessing the HN api for new stories

url = 'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty'
new_stories = requests.get(url)
new_stories.raise_for_status()
id_list = json.loads(new_stories.text)

counter_dict = {}
for num in range(len(id_list)):
    counter_dict[num+1] = 0


# accessing the necessary data from these stories.

while True:
    for number, item_id in enumerate(id_list[0:items_tracked]):
        url =('https://hacker-news.firebaseio.com/v0/item/%s.json?print=pretty' % item_id)
        item_post = requests.get(url)
        item_post.raise_for_status()
        hn_item = json.loads(item_post.text)
        ''' and hn_item['score'] >= 3'''
        if hn_item['type'] == 'story':
            score = hn_item.get('score', 0)
            title = hn_item.get('title', 0)
            id = hn_item.get('id', 0)
            file = "hn_score_item%s.txt" % (number+1)
            file_to_list(file,number+1,title,id,score)
    count_for_plotting += 1
    print("working #%s" % count_for_plotting)
    if user_input_plot.startswith("y"):
        if count_for_plotting % 3 == 0:
            plot()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    plt.close()
