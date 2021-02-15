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

import speech_recognition as sr

import sphinxbase
import pocketsphinx

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Reading Audio file as source
# listening the audio file and store in audio_text variable

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio.wav')
with sr.AudioFile(AUDIO_FILE) as source:
    
    audio_text = r.listen(source)

LONG_AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio-original.wav')
with sr.AudioFile(LONG_AUDIO_FILE) as source:
    
    long_audio_text = r.listen(source)


#######-----Sphinx---------#####
# use the audio file as the audio source

print('\nTesting Sphinx...\n')

r = sr.Recognizer()
with sr.AudioFile(LONG_AUDIO_FILE) as source:
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
    long_audio = AudioSegment.from_mp3(filename)
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