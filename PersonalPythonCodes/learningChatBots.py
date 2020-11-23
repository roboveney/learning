#!/usr/bin/env python3.6

import requests
import string
from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup
import subprocess
from gtts import gTTS
import pyttsx3


def playSound(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()

def textPlay(text):
    language = 'en'
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("TTS.wav")
    playSound("TTS.wav")
    
def usePTTS(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') #not much real difference in these voices
    engine.setProperty('voice', voices[22].id)
    engine.say(text)
    engine.runAndWait()

def parseWebsite(query,index=0):
    search_result_list = list(search(query))

    page = requests.get(search_result_list[index])

    tree = html.fromstring(page.content)

    soup = BeautifulSoup(page.content, features="lxml")

    article_text = ''
    article = soup.findAll('p')
    for element in article:
        article_text += '\n' + ''.join(element.findAll(text = True))
    article_text = article_text.replace('\n', '')
    first_sentence = article_text.split('.')
    first_sentence = first_sentence[0]
    
    #print("the first sentence is...\n %s" %first_sentence)
    
    #chars_without_whitespace = first_sentence.translate(
    #    { ord(c): None for c in string.whitespace }
    #)    
    return(first_sentence)

def chatbot_query(query):
    fallback = 'Sorry, I cannot think of a reply for that.'
    result = ''

    try:
        text = parseWebsite(query,index=0)
        
        if len(text) > 0:
            result = text            
        else:
            result = fallback
        return result
        #print(result)
    except:
        if len(result) == 0: result = fallback
        return result
        #print(result)


while True:
    question = input('You: ')
    if question == 'quit':
        break
    out = chatbot_query(question)
    print('Bot: ', out)
    usePTTS(out)
