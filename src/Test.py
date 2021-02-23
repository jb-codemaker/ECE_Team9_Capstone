import pandas as pd
from matplotlib import pyplot as plt

Word_Count = pd.read_csv("data/Sample_csv.csv")
print(Word_Count)


Professor = Word_Count[Word_Count['Speaker'] == 'A']
Students = Word_Count[Word_Count['Speaker'] == 'B']
Minute_A = Professor['Minute']
Speaker_A = Professor['WPM']
Minute_B = Students['Minute']
Speaker_B = Students['WPM']


plt.plot(Minute_A,Speaker_A)
plt.plot(Minute_B, Speaker_B)
plt.xlabel('Minutes')
plt.ylabel('Word/Min')
plt2=plt.twinx()
plt2.plot = (Word_Count['Attentiveness'], Word_Count['Minute'])
plt2.set_ylabel('Attentiveness')
plt.title('Word numbers and Attentiveness')
plt.show()



