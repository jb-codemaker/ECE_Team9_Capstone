import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import CheckButtons

# Enter CSV to process:
word_count = pd.read_csv(r"/home/leo/Projects/ECE_Team9_Capstone/data/Sample_csv.csv")
 
professor = word_count[word_count['Speaker'] == 'A']
students = word_count[word_count['Speaker'] == 'B']
minute_A = professor['Minute']
speaker_A = professor['WPM']
minute_B = students['Minute']
speaker_B = students['WPM'] 

df1 = pd.DataFrame(speaker_A)
df1.columns =['AWPM'] 
df2 = pd.DataFrame(speaker_B)
df2.columns =['BWPM'] 

# Merge df1 and df2
result = pd.concat([df1, df2], axis=1)
result = result.reset_index(drop=False)

# Replace NaN values with zeroes:
result.fillna(0, inplace=True)
result = result.astype(int)


fig, ax1 = plt.subplots()
plt.grid()
plt.title('Word numbers and Attentiveness')



# Start to plot
#ax1.set_xlabel('Minutes')
#ax1.set_ylabel('Word/Min',color = 'blue')
ax1.tick_params(axis='y', colors= 'blue')

P1, = ax1.plot(result['index'], result['AWPM'],'--', color ='blue',label = 'Professor', visible = True)
P2, = ax1.plot(result['index'], result['BWPM'],color ='blue',label = 'Students', visible = True)

ax2 = ax1.twinx()
ax3 = ax1.twinx()
#
ax2.tick_params(axis='y', colors='green')
#ax3.set_ylabel('Ranked Complexity',color ='red')
ax3.tick_params(axis='y', colors='red')

#adjust Ranked Complexity y axis and y label
ax3.yaxis.set_ticks_position('left')
ax3.yaxis.set_label_position('left')

P3, = ax2.plot(word_count['Minute'], word_count['Attentiveness'], color = 'green',label = 'complex', visible = True)
P4, = ax3.plot(word_count['Minute'], word_count['Ranked Complexity'], color = 'red',label = 'Ranked Complexity', visible = True)

# leave this here
plt.subplots_adjust(left=0.25, bottom=0.1,right=0.95, top=0.95) 
labels = ['Professor Word Count', 'Students Word Count', 'Students Attentiveness', 'Ranked Complexity' ]
activated = [True, True, True, True]
axCheckButton  = plt.axes([0.03,0.4,0.15,0.15])
chxbox = CheckButtons(axCheckButton, labels, activated)

def set_visable(label):
    index = labels.index(label)
    lines = [P1, P2, P3, P4]
    lines[index].set_visible(not lines[index].get_visible())

    if label == 'Students Attentiveness':
        activated[2] = not(activated[2])
    if label == 'Professor Word Count':
        activated[0] = not(activated[0])

    
    if activated[2] == True:
        ax2.set_ylabel('Attentiveness',color ='green' , visible = True)
    else:
        ax2.set_ylabel('Attentiveness',color ='green' , visible = False)

    if activated[0] == True:
        ax1.set_ylabel('Word/Min',color = 'blue', visible =True)
        ax1.axes.yaxis.set_visible(True)
    else:
        ax1.set_ylabel('Word/Min',color = 'blue',visible = False)
        ax1.axes.yaxis.set_visible(False) 

    plt.draw()



chxbox.on_clicked(set_visable)

plt.show()

