import matplotlib.pyplot as plt
from matplotlib import style
from pathlib import Path



### Reading the scores of Hacker News articles from text files generated with hn_scores_plotting
### and plotting them in a graph.
### Note: All txt files must have the same number of items and a string(titel) as first index.
### Note: nummeration of the txt files must be ascending without interuption (i.e. 1, 2, 3; not 1, 4, 5)

items_tracked = 0 # will be automatically augmented.
major_list = [] # list that will contain the lists with scores for each item

# function to read .txt file with scores and to append scores as list to the major_list
def file_to_list(file):
    list = []
    with open(file, "r") as scores:
        for line in scores:
            list.append(line.strip().split(','))
        score_list = [item for sublist in list for item in sublist]
        major_list.append(score_list)


# creating variable names for files with scores to read and handing them to the file_to_list function

for number in range(1,21): # if more than 20 txt files, adjust the number
    file = "hn_score_item%s.txt" % number
    my_file = Path(file)
    if my_file.is_file():
        items_tracked += 1
        file_to_list(file)
    else:
        break

for number in range(1,items_tracked+1):
    file = "hn_score_item%s.txt" % number
    file_to_list(file)

# creating a timpestamp list with equal number of digits as in the score lists - will be x axis
timestamp = []
for item in range(len(major_list[0])):
    timestamp.append(item)

# styles for plotting

style.use('fivethirtyeight')

font = {'family' : 'arial',
        'weight' : 'light',
        'size'   : 8}

plt.rc('font', **font)

# creating the graphs

print(items_tracked)

for index in range(items_tracked):
    plt.plot(timestamp[2:],major_list[index][2:], label=major_list[index][0])



plt.xlabel('time (in minutes)')
plt.ylabel('Score')
plt.title('Scores over time for selected Hacker News articles')
plt.legend()
plt.show()
