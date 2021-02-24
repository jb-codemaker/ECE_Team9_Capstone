import pandas as pd
from matplotlib import pyplot as plt
from numpy import arange

word_count = pd.read_csv("data/Sample_csv.csv")
#print(word_count)


professor = word_count[word_count['Speaker'] == 'A']
students = word_count[word_count['Speaker'] == 'B']
#print(professor)
#print(students)

max_min = word_count['Minute'].max()+1
minutes = list(range(max_min))


new_index = pd.Index(arange(0,20,1),name='Minute')
professor.set_index('Minute').reindex(new_index)
professor.set_index('Minute').reindex(new_index).reset_index()

print(professor)
'''
for i in range(len(Minutes)):
    if professor.isin([i]):
        print("FOUND")
'''

print(minutes)



minute_A = professor['Minute']
speaker_A = professor['WPM']
minute_B = students['Minute']
speaker_B = students['WPM'] 




fig, ax1 = plt.subplots()


plt.title('Word numbers and Attentiveness')
ax1.set_xlabel('Minutes')
ax1.set_ylabel('Word/Min')
ax1.plot(minute_A, speaker_A)
ax1.plot(minute_B, speaker_B)



ax2=ax1.twinx()

ax2.set_ylabel('Attentiveness')
ax2.plot = (word_count['Attentiveness'])
ax2.tick_params()

plt.show()







