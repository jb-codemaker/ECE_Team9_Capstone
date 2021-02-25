# Project: An Algorithmic Teaching Practices and Classroom Activities Tool to Improve Education
#
# Authors: Joshua Blazek, Leo Garcia, Naiqi Yao, and Jinghan Zhang
#
# Sponsor: Christof Teuscher and teuscher-lab.com
#
# Ownership: See https://github.com/jb-codemaker/ECE_Team9_Capstone for license details
#
#
# This file: Counts spoken words.

import os
import sys

from os import path

import speech_recognition as sr # Hidden Markov Model (HMM), deep neural network model

import sphinxbase

from pydub import AudioSegment
from pydub.utils import make_chunks

import csv
import string

from datetime import datetime

#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio-original.wav')
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio.wav')

myaudio = AudioSegment.from_file(AUDIO_FILE , "wav") 
chunk_length_ms = 60000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one min

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    print ("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")

with open('audio_data_csv.csv', mode='w', newline='') as audio_data_csv:
    audio_data_csv_writer = csv.writer(audio_data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    audio_data_csv_writer.writerow(['Translator', 'Minute', 'Speaker', 'WPM', 'Text'])

'''
##------------------resemblyzer---------#####

from resemblyzer import preprocess_wav, VoiceEncoder
from demo_utils import *
from pathlib import Path

## Get reference audios
wav = preprocess_wav(AUDIO_FILE)

# Cut some segments from single speakers as reference audio
# Speaker times are in seconds [beginning, end]
segments = [[1, 5]]
speaker_names = ["A"]
speaker_wavs = [wav[int(s[0] * 16000):int(s[1] * 16000)] for s in segments]
  
    
# Rate of 16, meaning that an 
# embedding is generated every 0.0625 seconds. It is good to have a higher rate for speaker 
# diarization, but it is not so useful for when you only need a summary
# Forcing this on CPU, because it uses a lot of RAM and most GPUs 
# won't have enough. There's a speed drawback, but it remains reasonable.
encoder = VoiceEncoder("cpu")
print("Running the continuous embedding on cpu, this might take a while...")
_, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)


# Get the continuous similarity for every speaker. It amounts to a dot product between the 
# embedding of the speaker and the continuous embedding of the interview
speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in 
                   zip(speaker_names, speaker_embeds)}


## Run the interactive demo
interactive_diarization(similarity_dict, wav, wav_splits)
##--------------------- end resemblyzer----------###
'''


now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Start of Google Time =", current_time)

#######  Google test #############
i = 0
print ("-------------------------------------------------")
print ("Testing google's offline recognizer with chunks")
print ("-------------------------------------------------")
set_ambient_noise = True

#sr out of for chunk scope to retain ambient noise levels
r = sr.Recognizer()
for chunk in chunks:
    #chunk_silent = AudioSegment.silent(duration = 10)
    #audio_chunk = chunk_silent + chunk + chunk_silent
    chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
    filename = 'chunk'+str(i)+'.wav'
    print("Processing minute "+str(i))
    file = filename
    #r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        # Set ambient noise level on 1st chunk only
        if set_ambient_noise:
            r.adjust_for_ambient_noise(source, duration=2)
            set_ambient_noise = False
        audio_listened = r.record(source)
    try:
        rec = r.recognize_google(audio_listened, language='en-US', show_all=False)
        print (rec)
        word_count = str(rec).split()
        with open('audio_data_csv.csv', mode='a', newline='') as audio_data_csv:
            audio_data_csv_writer = csv.writer(audio_data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            audio_data_csv_writer.writerow(['Google', str(i), 'A', len(word_count), rec])
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except:
        rec = r.recognize_google(audio_listened,)#show_all=True)
        print(rec,type(rec))
        word_count = str(rec).split()
        with open('audio_data_csv.csv', mode='a', newline='') as audio_data_csv:
            audio_data_csv_writer = csv.writer(audio_data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            audio_data_csv_writer.writerow(['Google', str(i), 'A', len(word_count), rec])

    i += 1
############ End Google test ###########

# Print time delta without decimals
process_duration = str(datetime.now() - now).split('.')[0]
print('\nGoogle took ', process_duration, ' to process')

now = datetime.now()

############ Testing Sphinx ##########
i = 0
print ("\n-------------------------------------------------")
print ("Testing Sphinx recognizer with chunks")
print ("-------------------------------------------------")
for chunk in chunks:
    #chunk_silent = AudioSegment.silent(duration = 10)
    #audio_chunk = chunk_silent + chunk + chunk_silent
    chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
    filename = 'chunk'+str(i)+'.wav'
    print("Processing minute "+str(i))
    file = filename
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        #r.adjust_for_ambient_noise(source)
        audio_listened = r.record(source)
    try:
        rec = r.recognize_sphinx(audio_listened)
        print (rec)
        word_count = str(rec).split()
        with open('audio_data_csv.csv', mode='a', newline='') as audio_data_csv:
            audio_data_csv_writer = csv.writer(audio_data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            audio_data_csv_writer.writerow(['Sphinx', str(i), 'A', len(word_count), rec])
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    except:
        rec = r.recognize_sphinx(audio_listened,show_all=True)
        print(rec,type(rec))
        word_count = str(rec).split()
        with open('audio_data_csv.csv', mode='a', newline='') as audio_data_csv:
            audio_data_csv_writer = csv.writer(audio_data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            audio_data_csv_writer.writerow(['Sphinx', str(i), 'A', len(word_count), rec])
    i += 1

######### End sphinx test ##########

# Print time delta without decimals
process_duration = str(datetime.now() - now).split('.')[0]
print('\nSphinx took ', process_duration, ' to process')


# speaker discrimination / diarization