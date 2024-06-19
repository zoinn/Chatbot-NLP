#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic chatbot design --- for your own modifications
"""
import tkinter.filedialog

import nltk
import pyttsx3
import sys
from Cosine_Similarity import Cosine_Similarity
from First_Order_Logic import FOL
from Model_Tester import recogniseImage
import wikipedia
import tkinter as tk
from tkinter import filedialog

import json, requests
#insert your personal OpenWeathermap API key here if you have one, and want to use this feature
APIkey = "5403a1e0442ce1dd18cb1bf7c40e776f"
import time
time.clock = time.time
import aiml
class TTSStream:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('engine', 'sapi5')
        self.engine.setProperty('key', 'single')

    def write(self, text):
        sys.__stdout__.write(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def flush(self):
        pass

# Create a Kernel object. No string encoding (all I/O is unicode)
kern = aiml.Kernel()
kern.setTextEncoding(None)
# Creates First order logic Object
F = FOL()
# Use the Kernel's bootstrap() method to initialize the Kernel. The
# optional learnFiles argument is a file (or list of files) to load.
# The optional commands argument is a command (or list of commands)
# to run after the files are loaded.
# The optional brainFile argument specifies a brain file to load.
kern.bootstrap(learnFiles="ChatBot_Main.xml")
#######################################################
# Welcome user
print("Welcome to this chat bot. Please feel free to ask questions from me!")
#######################################################
# Main loop
#######################################################
while True:
    #get user input
    try:
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break
    #pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'
    #activate selected response agent
    if responseAgent == 'aiml':
        answer = kern.respond(userInput)
    #post-process the answer for commands
    if answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            print(params[1])
            break
        elif cmd == 1:
            try:
                wSummary = wikipedia.summary(params[1], sentences=3,auto_suggest=False)
                print(wSummary)
            except:
                print("Sorry, I do not know that. Be more specific!")
        elif cmd == 2:
            succeeded = False
            api_url = r"http://api.openweathermap.org/data/2.5/weather?q="
            response = requests.get(api_url + params[1] + r"&units=metric&APPID="+APIkey)
            if response.status_code == 200:
                response_json = json.loads(response.content)
                if response_json:
                    t = response_json['main']['temp']
                    tmi = response_json['main']['temp_min']
                    tma = response_json['main']['temp_max']
                    hum = response_json['main']['humidity']
                    wsp = response_json['wind']['speed']
                    wdir = response_json['wind']['deg']
                    conditions = response_json['weather'][0]['description']
                    print("The temperature is", t, "Â°C, varying between", tmi, "and", tma, "at the moment, humidity is", hum, "%, wind speed ", wsp, "m/s,", conditions)
                    succeeded = True
            if not succeeded:
                print("Sorry, I could not resolve the location you gave me.")
        elif cmd == 99:
            CS = Cosine_Similarity()
            most_similiar_index = CS.calculate_cosine(userInput)
            if most_similiar_index is not None:
                print(CS.get_answer(most_similiar_index))
            else:
                print("Sorry I dont know that one")

        elif cmd == 101:
            object, subject, expr = F.processInput(params)
            if F.addNewStatement(params):
                print('OK, I will remember that', object, 'is', subject)
            else:
                print("This contradicts what I know")

        elif cmd == 102:
            object, subject, expr = F.processInput(params)
            p, n = F.prove(params)
            if p:
                print('Yes I remember that', object, 'is', subject+'.')
            elif n:
                print('This is incorrect according to my knowledge.')
            else:
                print('I have no knowledge of this.')

        elif cmd == 103:
            object, subject, expr = F.processFalseInput(params)
            if F.addNewFalseStatement(params):
                print('OK, I will remember that', object, 'is not', subject)
            else:
                print("This contradicts what I know")

        elif cmd == 104:
            object, subject, expr = F.processFalseInput(params)
            p, n = F.proveFalse(params)
            if n:
                print('Yes I remember that', object, 'is not', subject+'.')
            elif p:
                print('This is incorrect according to my knowledge.')
            else:
                print('I have no knowledge of this.')

        elif cmd == 111 or cmd == 112:
            try:
                window = tk.Tk()
                window.withdraw()
                path = filedialog.askopenfilename(parent=window, title='Choose an Image')
                window.destroy()
                if recogniseImage(path) == "dog":
                    print("This is an image of a dog")
                else:
                    print("This is not an image of a dog")
            except:
                print("Please enter a valid file format")
        elif cmd == 200:
            animal, breed = F.getQuestion()
            print("Is this a dog breed or not:",breed+"?")
            answer = input("Enter (Y/N): ")
            if answer.lower() == "y" and animal == "dog":
                print("Correct Answer!", breed.capitalize(),"is a", animal.capitalize())
            elif answer.lower() == "n" and animal == "cat":
                print("Correct Answer!", breed.capitalize(),"is a", animal.capitalize())
            elif answer.lower() == "n" and animal == "dog":
                print("Incorrect Answer.", breed.capitalize(),"is a", animal.capitalize())
            elif answer.lower() == "y" and animal == "cat":
                print("Incorrect Answer.", breed.capitalize(), "is a", animal.capitalize())
            else:
                print("Invalid Answer")
        elif cmd == 300:
            sys.stdout = TTSStream()
            print("Text To Speech: On")

        elif cmd == 301:
            sys.stdout = sys.__stdout__
            print("Text To Speech: Off")

    else:
        print(answer)
