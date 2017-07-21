import matplotlib.pyplot as plt
import statistics
from collections import defaultdict
import requests
import json
import datetime
from wordcloud import WordCloud
import random

# Read more about what this script does here: http://meshedsociety.com/analyzing-the-hacker-news-front-page-as-a-python-beginner/

plt.style.use('ggplot')
color = '#0580ae'

# reading the data from the csv into a list of lists.

hn_result_list_with_post = []

with open('hn_entries.csv', 'r') as f:
    for line in f:
        hn_result_list_with_post.append(line.strip().split(';'))

# filtering out selected posts with certain criteria #

hn_result_list_with_post = [post for post in hn_result_list_with_post[1:] if "YC" not in post[0] if post[1] != "1" if int(post[1]) < 500]



'''bin_boundaries = [(0, 15),(15, 60),(60,120),(120,300),(300, 500)]
bin_counts = defaultdict(int)
minutes_agr = defaultdict(int)

for post in hn_result_list_with_post:
    for low, high in bin_boundaries:
        if low < int(post[3]) <= high:
            print(post[3])
            print(post[1])
            minutes_agr[(low, high)] += int(post[1])
            bin_counts[(low, high)] += 1

print(minutes_agr[(15, 60)])
print(bin_counts[(15, 60)])

print(round(minutes_agr[(0, 15)]/bin_counts[(0, 15)],1))
print(round(minutes_agr[(15, 60)]/bin_counts[(0, 15)],1))
print(round(minutes_agr[(60, 120)]/bin_counts[(0, 15)],1))
print(round(minutes_agr[(120, 300)]/bin_counts[(0, 15)],1))
print(round(minutes_agr[(300, 500)]/bin_counts[(0, 15)],1))'''



sum1 = 0
count1 = 0
sum2 = 0
count2 = 0
sum3 = 0
count3 = 0
sum4 = 0
count4 = 0
sum5 = 0
count5 = 0


for post in hn_result_list_with_post:
    if int(post[3]) <= 15:
        sum1 += int(post[1])
        count1 += 1
        total1 = round(sum1/count1, 1)
    if int(post[3]) < 15 <= 60:
        sum2 += int(post[1])
        count2 += 1
        total2 = round(sum2/count2, 1)
    if int(post[3]) < 60 <= 120:
        sum3 += int(post[1])
        count3 += 1
        total3 = round(sum3/count3, 1)
    if int(post[3]) < 120 <= 300:
        sum4 += int(post[1])
        count4 += 1
        total4 = round(sum4/count4, 1)
    if int(post[3]) < 300:
        sum5 += int(post[1])
        count5 += 1
        total5 = round(sum5/count5, 1)


print(total1)
print(total2)
print(total3)
print(total4)
print(total5)





# functions

def count_posts():
    count = 0
    for post in hn_result_list_with_post:
        count += 1
    return count

def highest_score():
    highest_score_list = []
    for item in hn_result_list_with_post:
        highest_score_list.append(int(item[1]))

    global score_dict_aggregate
    score_dict_aggregate = {}

    highest_score = int(max(highest_score_list))
    for number in range(highest_score+1):
        score_dict_aggregate[number] = 0

    for post in hn_result_list_with_post:
        score_dict_aggregate[int(post[1])] += 1

def score_distribution():
    scores_list = []
    number_of_posts_list = []
    highest_score()
    count_excess_value = 0 # number of posts that go beyond the x-axis scale
    for key, value in score_dict_aggregate.items():
        if key <= 20:
            scores_list.append(key)
            number_of_posts_list.append(value)
        if key > 20:
            count_excess_value += value

    scores_list.append('21+')
    number_of_posts_list.append(count_excess_value)
    plt.xlabel('Score', fontsize=8)
    plt.ylabel('Number of posts out of total: %s' % count_posts(), fontsize=8)
    plt.bar(range(len(number_of_posts_list)), number_of_posts_list, align='center', color=color)
    my_xticks = scores_list #here custom ticks could be used
    plt.xticks(range(len(number_of_posts_list)), my_xticks, size='small')
    plt.title('Score at which an item hit Hacker News front page, July 2017', fontsize=10)
    plt.show()

def minute_distribution():
    minutes_list = [] # getting all the minute values from the csv, appending it to a list
    for post in hn_result_list_with_post:
        minutes_list.append(post[3])
    minutes_list = list(map(int, minutes_list)) # converting all list values into int

    bin_boundaries = [(0, 15),(15, 60),(60,120),(120,300),(300, max(minutes_list))]
    #my_xticks = [bin_boundaries[y-1] for y in bin_count_list]
    my_xticks = ["1-15", "16-60", "61-120", "121-300", "301+"] #can be automatically generated with code on line above
    bin_counts = defaultdict(int)

    for value in minutes_list:
        for low, high in bin_boundaries:
            if low < value <= high:
                bin_counts[(low, high)] += 1

    bin_count_list = [i+1 for i in range(len(bin_boundaries))]

    count_per_bin_for_graph = [bin_counts[bin_boundaries[a]] for a in range(len(bin_boundaries))]

    plt.xlabel('Minutes from posting to front page', fontsize=8)
    plt.ylabel('Number of posts (total analyzed: %s)' % count_posts(),fontsize=8)
    plt.bar(bin_count_list, count_per_bin_for_graph, align='center', color=color)
    plt.xticks(bin_count_list, my_xticks, size='small')
    plt.title('Time until an article hit the Hacker News front page, July 2017', fontsize=10)


    '''for a,b in zip(bin_count_list, count_per_bin_for_graph):
        plt.text(a, b, str(b), fontsize=8)'''
        #showing the numbers directly at the bars
    plt.show()


def contributor_distribution():
    name_dict = {}
    for post in hn_result_list_with_post:
        if post[4] in name_dict:
            name_dict[post[4]] += 1
        else:
            name_dict[post[4]] = 1

    contribution_dict = {}

    contribution_list = []
    for contribution in name_dict.values():
        if contribution in contribution_dict:
            contribution_dict[contribution]+= 1
        else:
            contribution_dict[contribution]= 1

    contribution_list = []
    for number in contribution_dict.values():
        contribution_list.append(number)

    sum_i = 0
    for i in contribution_list[2:]:
        sum_i += i

    new_contribution_list = [contribution_list[0],contribution_list[1],sum_i]


    labels = [r'By user with 1 front page contribution', r'By user with 2 front page contributions',
    r'By user with 3 or more front page contributions']

    plt.pie(new_contribution_list,
        #labels=activity_list,
        colors=(color,'#75c9e8','#0d546e'),
        startangle=90,
        explode=(0.1,0.1,0.1),
        autopct='%1.1f%%',
        pctdistance=0.625)

    plt.title('Number of front page posts per user, July 2017', fontsize=10)
    plt.legend(labels, fontsize=8)
    plt.text(0, -1.5,'Based on %s Hacker News front page posts.' % count_posts(),
     horizontalalignment='center',
     verticalalignment='center', fontsize=8)
    plt.show()

def wordcloud_color(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(196, 94%%, %d%%)" % random.randint(20, 99)


def wordcloud_all():
    string = ''
    count = 0
    for post in hn_result_list_with_post:
        count += 1
        string += post[0]


    wordcloud = WordCloud(max_font_size=40).generate(string)
    default_colors = wordcloud.to_array()
    plt.figure()
    plt.imshow(wordcloud.recolor(color_func=wordcloud_color, random_state=3),interpolation="bilinear")
    plt.axis("off")
    plt.show()



def wordcloud_15_minutes():

    string = ''
    count = 0
    for post in hn_result_list_with_post:
        if int(post[3]) > 0:
            if int(post[3])<= 15:
                count += 1
                string += post[0]
    print(count)

    wordcloud = WordCloud(max_font_size=40).generate(string)
    default_colors = wordcloud.to_array()
    plt.figure()
    plt.imshow(wordcloud.recolor(color_func=wordcloud_color, random_state=3),interpolation="bilinear")
    plt.axis("off")
    plt.show()



### Functions to run for plots

score_distribution()
minute_distribution()
#contributor_distribution()
#wordcloud_all()
#wordcloud_15_minutes()



'''## UNUSED
## analzying user karma for posts based on time to frontpage
rechnen = 0
fast_poster_list = []
for post in hn_result_list_with_post:
    if int(post[3]) > 15:
        if int(post[3])<= 30:
            url = ("https://hacker-news.firebaseio.com/v0/user/%s.json?print=pretty" % post[4])
            username = requests.get(url)
            username.raise_for_status()
            user = json.loads(username.text)
            karma = user.get('karma', 0)
            fast_poster_list.append(karma)

fast_poster_list = list(map(int, fast_poster_list))
print(int(sum(fast_poster_list) / int(len(fast_poster_list))))'''
