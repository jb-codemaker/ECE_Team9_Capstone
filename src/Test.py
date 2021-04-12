import pandas as pd
from matplotlib import pyplot as plt


# Enter CSV to process:
word_count = pd.read_csv("data/Sample_csv.csv")

#print(word_count)

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
#print(result)

# Label the plot
fig, ax1 = plt.subplots()
plt.grid()
plt.title('Word numbers and Attentiveness')




# Start to plot
ax1.set_xlabel('Minutes')
ax1.set_ylabel('Word/Min')
ax1.plot(result['index'], result['AWPM'],label = 'Professor')
ax1.plot(result['index'], result['BWPM'],label = 'Students')

# Put legend on plot
plt.legend(loc = (0,1.05))

#Plot Attentiveness using different y-axis
ax2=ax1.twinx()

ax2.set_ylabel('Attentiveness',color ='green')
ax2.plot(word_count['Minute'],word_count['Attentiveness'],'-*', color = 'green',label = 'Attentiveness')

# Put legend on plot
plt.legend(loc = (0,1))

plt.show()
