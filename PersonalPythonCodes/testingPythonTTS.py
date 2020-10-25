#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:12:43 2020

@author: cveney
"""
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices') #not much real difference in these voices
engine.setProperty('voice', voices[22].id)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()