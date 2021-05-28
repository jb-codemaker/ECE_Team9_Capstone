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
import glob     # for file listing

import speech_recognition as sr # Hidden Markov Model (HMM), deep neural network model

import sphinxbase

from pydub import AudioSegment
from pydub.utils import make_chunks

import csv
import string

from datetime import datetime

from resemblyzer import preprocess_wav, VoiceEncoder
from diarize import *
from pathlib import Path

import logging  # logging instead of printing

# Initiate logging
# Create logfile
logging.basicConfig(filename='run.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Let us Create an object 
logger = logging.getLogger()

# Set level of logger
logger.setLevel(logging.INFO) 

# Takes in an array of floats to populate a csv file
# speaker diarization
# 0.0625 seconds per reading with current settings (rate setting)
def populate_speaker(diarize_file, similarity_dict):

    logger.info("Populating diarize csv...")
    with open(diarize_file, mode='w', newline='') as audio_diarize_csv:
        audio_diarize_csv_writer = csv.writer(audio_diarize_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        audio_diarize_csv_writer.writerow(['Second', 'Speaker', 'Prof. Confidence'])
    
    # extract Professor values into a list for
    # ease of use
    # Get first value of dictionary
    confidence_values = list(similarity_dict.items())[0][1]

    # iterate for a seconds count
    t = 0
    # iterate over confidence levels for each embedding and populate csv
    for confidence in confidence_values:
        #iterate for our time
        t = t + 1

        # If confidence is > 0.75 then it's the professor
        if confidence > 0.75:
            with open(diarize_file, mode='a', newline='') as audio_diarize_csv:
                audio_diarize_csv_writer = csv.writer(audio_diarize_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                audio_diarize_csv_writer.writerow([t * 0.0625, 'Professor', confidence])
        elif confidence < 0.75:
            with open(diarize_file, mode='a', newline='') as audio_diarize_csv:
                audio_diarize_csv_writer = csv.writer(audio_diarize_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                audio_diarize_csv_writer.writerow([t * 0.0625, 'Student', confidence])

#--------- End populate speaker ---------#


def audio_analyze():
    if os.name == 'posix':
        delimiter = '/'
    else: 
        delimiter = '\\'

    current_directory = os.getcwd()
    data_directory = os.path.abspath(os.path.join(current_directory, os.pardir + delimiter + 'data'))

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), '0-output-audio.wav')

    myaudio = AudioSegment.from_file(AUDIO_FILE , "wav") 
    chunk_length_ms = 10000 # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks from audio file

    # Remove old chunks
    for filename in glob.glob(data_directory + delimiter + 'chunk*'):
        os.remove(filename)

    # Create new chunks
    for i, chunk in enumerate(chunks):
        chunk_name = data_directory + delimiter + "chunk{0}.wav".format(i)
        chunk.export(chunk_name, format="wav")

    with open(data_directory + delimiter + 'audio_wpm_csv.csv', mode='w', newline='') as audio_wpm_csv:
        audio_wpm_csv_writer = csv.writer(audio_wpm_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        audio_wpm_csv_writer.writerow(['Second', 'WPM', 'Text'])

    ##------------------resemblyzer---------#####
    ## Open source project from https://github.com/resemble-ai/Resemblyzer

    ## Get reference audios
    wav = preprocess_wav(AUDIO_FILE)

    # Cut some segments from single speakers as reference audio
    # Speaker times are in seconds [beginning, end]
    # Can diarize multiple speakers (e.g. students and professor)
    # Segments and speaker names are ordered specific
    segments = [[1, 5]]
    speaker_names = ["Professor"]

    # This assumes the speaker portion was appended to the beginning of the audio
    # file but it could also be passed in a seperate file
    speaker_wavs = [wav[int(s[0] * 16000):int(s[1] * 16000)] for s in segments]
    
        
    # Rate of 16 = an embedding every 0.0625 seconds.
    # Higher rate = better for speaker 
    # diarization, but it is not so useful for when you only need a summary
    # Forcing this on CPU, because it uses a lot of RAM and most GPUs 
    # won't have enough. There's a speed drawback, but it remains reasonable.
    # The rate also determines how many floats will populate the array.
    # For example. A 14 second audio file would give ~239 readings at 0.0625 secs.
    encoder = VoiceEncoder("cpu")
    logger.info("Continuous embedding running on cpu...")
    _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)

    # Get the continuous similarity for every speaker. This is a dot product between the 
    # embedding of the speaker and the continuous embedding of the whole audio file
    speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
    similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in 
                    zip(speaker_names, speaker_embeds)}

    # Produce 'audio_diarize_csv.csv'
    diarize_file =  data_directory + delimiter + 'audio_diarize_csv.csv'

    populate_speaker(diarize_file, similarity_dict)

    ## Run the interactive demo
    interactive_diarization(similarity_dict, wav, wav_splits)
    ##--------------------- end resemblyzer----------###

    now = datetime.now()

    ############ Testing Sphinx ##########
    i = 0
    second_count = 10
    logger.info("Sphinx recognizer with chunks")
    for chunk in chunks:
        filename = data_directory + delimiter + 'chunk'+str(i)+'.wav'
        logger.info("Processing chunk...")
        file = filename
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
            #r.adjust_for_ambient_noise(source)
            audio_listened = r.record(source)
        try:
            rec = r.recognize_sphinx(audio_listened)
            logger.info(rec)
            word_count = str(rec).split()
            with open(data_directory + delimiter + 'audio_wpm_csv.csv', mode='a', newline='') as audio_wpm_csv:
                audio_wpm_csv_writer = csv.writer(audio_wpm_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                audio_wpm_csv_writer.writerow([str(second_count), len(word_count), rec])
        except sr.UnknownValueError:
            logger.info("Sphinx could not understand audio")
        except sr.RequestError as e:
            logger.info("Sphinx error")
        except:
            rec = r.recognize_sphinx(audio_listened,show_all=True)
            word_count = str(rec).split()
            with open(data_directory + delimiter + 'audio_wpm_csv.csv', mode='a', newline='') as audio_wpm_csv:
                audio_wpm_csv_writer = csv.writer(audio_wpm_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                audio_wpm_csv_writer.writerow([str(i), len(word_count), rec])
        i += 1
        second_count += 10

    ######### End sphinx test ##########

    # Print time delta without decimals
    process_duration = str(datetime.now() - now).split('.')[0]
    duration = 'Sphink took ' + process_duration + ' to process'
    logger.info(duration)