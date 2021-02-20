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

#import sphinxbase
import pocketsphinx

from pydub import AudioSegment
from pydub.utils import make_chunks

import csv
import string

from datetime import datetime

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio-original.wav')

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


now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Start of Google Time =", current_time)

#######  Google test #############
i = 0
print ("-------------------------------------------------")
print ("Testing google's offline recognizer with chunks")
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
        rec = r.recognize_google(audio_listened)
        print (rec)
        word_count = str(rec).split()
        with open('audio_data_csv.csv', mode='a', newline='') as audio_data_csv:
            audio_data_csv_writer = csv.writer(audio_data_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            audio_data_csv_writer.writerow(['Google', str(i), 'A', len(word_count), rec])
    except:
        rec = r.recognize_google(audio_listened,show_all=True)
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


'''

def load_chunks(filename):
    long_audio = AudioSegment.from_wav(filename)
    audio_chunks = split_on_silence(
        long_audio, min_silence_len=1800,
        silence_thresh=-17
    )
    return audio_chunks

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Reading Audio file as source
# listening the audio file and store in audio_text variable


with sr.AudioFile(AUDIO_FILE) as source:
    
    audio_text = r.listen(source)

LONG_AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio-original.wav')
with sr.AudioFile(LONG_AUDIO_FILE) as source:
    
    long_audio_text = r.listen(source)


#######-----Sphinx---------#####
# use the audio file as the audio source

print('\nTesting Sphinx...\n')

#r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

#####------ End Sphinx test---------######


#####------ Start Google test---------######
# recoginize_() method will throw a request error if the API...
# ... is unreachable, hence using exception handling
print('\nTesting google speech...\n')

try:
    # using google speech recognition
    text = r.recognize_google(audio_text)
    print('Converting audio file into text.')
    print(text)
except:
    print('Did not work.  Possibly file too large.  Try again.')
#####------ End Google test---------######


#####------ Start split google test---------######

print('\nTesting google split file speech...\n')

from pydub import AudioSegment
from pydub.silence import split_on_silence

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio.wav')

recognizer = sr.Recognizer()

def load_chunks(filename):
    long_audio = AudioSegment.from_wav(filename)
    audio_chunks = split_on_silence(
        long_audio, min_silence_len=1800,
        silence_thresh=-17
    )
    return audio_chunks

for audio_chunk in load_chunks(AUDIO_FILE):
    audio_chunk.export("temp", format="wav")
    with sr.AudioFile("temp") as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Chunk : {}".format(text))
        except Exception as ex:
            print("Error occured")
            print(ex)
#####------ End split google test---------######
'''