import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import CheckButtons

def visualize(file_name):

    # Enter CSV to process:
    word_count = pd.read_csv(file_name)

    # Redefine the dataset
    professor = word_count[word_count['Speaker'] == 'A']
    students = word_count[word_count['Speaker'] == 'B']
    #minute_A = professor['Minute']
    speaker_A = professor['WPM']
    #minute_B = students['Minute']
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

    ### Start to plot
    fig, ax = plt.subplots()
    plt.grid()
    plt.yticks([])

    # Colorful Title
    fig.text(0.45, 0.95, "Word Count", ha="center", va="bottom", size="large",color="blue")
    fig.text(0.52, 0.95, "&", ha="center", va="bottom", size="large")
    fig.text(0.6, 0.95, "Ranked Complexity", ha="center", va="bottom", size="large" ,color="red")
    fig.text(0.68, 0.95, "&", ha="center", va="bottom", size="large")
    fig.text(0.75,0.95,"Attentiveness", ha="center", va="bottom", size="large",color="green")

    # Word Count 
    ax1 = ax.twinx()
    ax1.tick_params(axis='y', colors= 'blue')
    ax1.yaxis.set_ticks_position('left')
    ax1.yaxis.set_label_position('left')
    ax1.set_visible(False)

    # Attentiveness
    ax2 = ax1.twinx()
    ax2.tick_params(axis='y', colors='green')
    ax2.set_visible(False) 

    # Ranked Complexity
    ax3 = ax1.twinx()
    ax3.tick_params(axis='y', colors='red')
    ax3.set_visible(False)  
    ax3.yaxis.set_ticks_position('left')
    ax3.yaxis.set_label_position('left')

    # plot all the lines
    P1, = ax1.plot(result['index'], result['AWPM'],'--', color ='blue',label = 'Professor', visible = False)
    P2, = ax1.plot(result['index'], result['BWPM'],color ='blue',label = 'Students', visible = False)
    P3, = ax2.plot(word_count['Minute'], word_count['Attentiveness'], color = 'green',label = 'complex', visible = False)
    P4, = ax3.plot(word_count['Minute'], word_count['Ranked Complexity'], color = 'red',label = 'Ranked Complexity', visible = False)

    # Check Button
    plt.subplots_adjust(left=0.25, bottom=0.1,right=0.95, top=0.95) 
    labels = ['Professor Word Count', 'Students Word Count', 'Students Attentiveness', 'Ranked Complexity' ]
    activated = [False, False, False, False]
    axCheckButton  = plt.axes([0.03,0.4,0.15,0.15])
    chxbox = CheckButtons(axCheckButton, labels, activated)

    ### Active lines in different cases
    def set_visable(label):
        index = labels.index(label)
        lines = [P1, P2, P3, P4]
        lines[index].set_visible(not lines[index].get_visible())

        if label == 'Ranked Complexity':
            activated[3] = not(activated[3])

        if label =='Students Attentiveness':
            activated[2] = not(activated[2])

        if label =='Students Word Count':
            activated[1] = not(activated[1])

        if label =='Professor Word Count':
            activated[0] = not(activated[0])

        # Ranked Complexity
        if activated[3] == False:
            ax3.set_ylabel('Ranked Complexity',color ='red', visible = False)
            ax3.set_visible(False)
        else:
            ax3.set_ylabel('Ranked Complexity',color ='red', visible = True)
            ax3.set_visible(True)
            

        # Attentiveness 
        if activated[2] == False:
            ax2.set_ylabel('Attentiveness (%)',color ='green' , visible = False)
            ax2.set_visible(False) 
        else:
            ax2.set_ylabel('Attentiveness (%)',color ='green' , visible = True)
            ax2.set_visible(True) 

        # Professor and Students Word Count (share same y-axis)
        if activated[1] == False and activated[0] == False:
            ax1.set_ylabel('Professor Word Count',color ='blue' , visible = False)
            ax1.set_visible(False)  

        if activated[1] == False and activated[0] == True:
            ax1.set_ylabel('Professor Word Count',color ='blue' , visible = True)
            ax1.set_visible(True)

        if activated[1] == True and activated[0] == False:
            ax1.set_ylabel('Students Word Count',color ='blue' , visible = True)
            ax1.set_visible(True)
    
        if activated[1] == True and activated[0] == True:
            ax1.set_ylabel('Professor & Students Word Count',color ='blue' , visible = True)
            ax1.set_visible(True) 


        plt.draw()



    chxbox.on_clicked(set_visable)

    plt.show()

if __name__ == "__main__":

    visualize(r"ECE_Team9_Capstone\data\Sample_csv.csv")