#!/usr/bin/env python
# coding: utf-8
import numpy as np
import re
from sklearn.externals import joblib
from textstat.textstat import textstat
import nltk
import collections as ct
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
import xlrd
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
import json
import csv
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


# In[4]:

LIWC_JSON =  open("LIWC.json",'r')
LIWC = json.load(LIWC_JSON)

def gettingFeatures(plainText):
        plainText = plainText.lower()
        syllables = textstat.syllable_count(plainText)
        # sentences = textstat.sentence_count(plainText)
        sentences = len(sent_tokenize(plainText))

        # print(plainText)
        # print("\nnumber of syllables: " + str(syllables) + "\n")
        # print("\nnumber of sentences: " + str(len(sentences)) + "\n")
        
        #Count all punctuation
        AllPunc = 0
        punc = "!\',./:;<=>?_`{|}~"
        #"!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
        cd = {c:val for c, val in ct.Counter(plainText).items() if c in punc}
        for x in cd.values():
            AllPunc = AllPunc + x
        #number of commas
        Comma = 0
        Comma = plainText.count(",")
        #number of question marks
        QMark = 0
        QMark = plainText.count("?")
        #number of colons
        Colon = 0
        Colon = plainText.count(":")
        #number of dash
        Dash = 0
        Dash = plainText.count("-")
        #number of dash
        Parenth = 0
        Parenth = plainText.count("(") + plainText.count(")")
        
        #Short version to full words
        # mapping = [('can\'t', 'can not'), ('let\'s', 'let us'), ('isn\'t', 'is not'), ('i\'m', 'i am'), 
        #            ('don\'t', 'do not'), ('doesn\'t', 'does not'), ('that\'s' , 'that is'), ('i\'s' , 'it is'), 
        #            ('i\'ve' , 'i have'), ('wouldn\'t', 'would not'), ('it\'s', 'it is'), ('he\'s', 'he is')] 
        # for (k, v) in mapping:
        #     plainText = plainText.replace(k, v)
        
        # replace all the punctuations with empty space
        punctuation = "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
        for p in punctuation:
            if p != '\'':
                plainText = plainText.replace(p, ' ')

        text = plainText.split(" ")
        while text.count(''): text.remove('')
        
	#words / syllables / sentences count
        wordCount = len(text) 
        wordCount = 457
        
        try:
            #ReadabilityScore
            readabilityScore = 206.835 - 1.015 * (wordCount / sentences) - 84.6 * (syllables / wordCount)
            #ReadabilityGrade
            ReadabilityGrade = 0.39 * (wordCount / sentences) + 11.8 * (syllables / wordCount) - 15.59
        except:
            readabilityScore = 0
            ReadabilityGrade = 0
        #Direction Count
        #private String[] direction = {"here", "there", "over there", "beyond", "nearly", "opposite", "under", "above", "to the left", "to the right", "in the distance"};
        DirectionCount  = 0
        DirectionCount = text.count("here") + text.count("there") + plainText.count("over there") + text.count("beyond") + text.count("nearly") + text.count("opposite") + text.count("under") + plainText.count("to the left") + plainText.count("to the right") + plainText.count("in the distance")
        #Exemplify count
	#private String[] exemplify = {"chiefly", "especially", "for instance", "in particular", "markedly", "namely", "particularly", "including", "specifically", "such as"};
        Exemplify = 0
        Exemplify = text.count("chiefly") + text.count("especially") + plainText.count("for instance") + plainText.count("in particular") + text.count("markedly") + text.count("namely") + text.count("particularly")+ text.count("incluiding") + text.count("specifically") + plainText.count("such as")
        #Analytical thinking
        #Analytic = 0 #LIWC Analysis
        #Aunthenticity
        #Authentic  = 0 #LIWC Analysis
        #Emotional tone
        #Tone = 0 #LIWC Analysis
        try:
            #words per sentence (average)
            WPS = 0
            # parts = [len(l.split()) for l in re.split(r'[?!.]', plainText) if l.strip()]
            # WPS = sum(parts)/len(parts) #number of words per sentence
            numOfWords = len(text)
            numOfSentences = sentences
            WPS = numOfWords / numOfSentences
        except:
            WPS = 0
        #Six letter words
        Sixltr = 0
        # words = plainText.split()
        letter_count_per_word = {w:len(w) for w in text}
        for x in letter_count_per_word.values():
            if x >= 6:
                Sixltr = Sixltr + 1
        Sixltr = Sixltr / wordCount * 100
        #Function words
        function = 0
        #Pronouns
        pronoun = 0
        text_tokens = word_tokenize(plainText)
        result = nltk.pos_tag(text_tokens)
        # pronoun = len([ (x,y) for x, y in result if y  == "PRP" or y  == "PRP$"])/wordCount
        pronoun = len([x for x in text if x in LIWC["Pronoun"]])/wordCount * 100
        #Personal pronouns
        ppron = 0
        # ppron = len([ (x,y) for x, y in result if y  == "PRP" ])/wordCount
        ppron = len([x for x in text if x in LIWC["Ppron"]])/wordCount * 100
        #I
        i = 0
        i = len([x for x in text if x in LIWC["I"]])/wordCount * 100
        #You
        you = 0
        you = len([x for x in text if x in LIWC["You"]])/wordCount * 100
        #Impersonal pronoun "one" / "it"
        ipron = 0
        # ipron = (text.count("one") + text.count("it"))/wordCount
        ipron = len([x for x in text if x in LIWC["Ipron"]])/wordCount * 100
        #Prepositions
        prep = 0
        # prep = len([ (x,y) for x, y in result if y  == "IN" ])/wordCount
        prep = len([x for x in text if x in LIWC["Prep"]])/wordCount * 100
        #Verb
        verb = 0
        text_tokens = word_tokenize(plainText)
        result = nltk.pos_tag(text_tokens)
        # verb = len([ (x,y) for x, y in result if y  == "VB" or y  == "VBD" or y  == "VBG" 
        #                or y  == "VBN" or y  == "VBP" or y  == "VBZ"])/wordCount
        verb = len([x for x in text if x in LIWC["Verbs"]])/wordCount * 100
        #Auxiliary verbs do/be/have
        auxverb = 0
        # auxverb = (text.count("do") + text.count("does") + text.count("don´t") + text.count("doesn´t") + text.count("has") + text.count("have") + text.count("hasn´t")+ text.count("haven´t") + text.count("am") + text.count("are") +  text.count("is") + plainText.count("´m") + plainText.count("´re") +  plainText.count("´s"))/wordCount
        auxverb = len([x for x in text if x in LIWC["AuxVb"]])/wordCount * 100
        #Negations
        negate = 0
        # negate = text.count("not")/wordCount
        negate = len([x for x in text if x in LIWC["Negate"]])/wordCount * 100
        #Count interrogatives
        #interrog = 0 #LICW Analysis
        #Count numbers
        number = 0
        number = len([x for x in text if x in LIWC["Numbers"]])/wordCount * 100
        
        # prep = len([ (x,y) for x, y in result if y  == "CD" ])/wordCount
        #Cognitive processes
        #cogproc = 0 #LIWC Analysis
        #Cause relationships
        #cause = 0 #LIWC Analysis
        #Discrepencies
        #discrep = 0 #LIWC Analysis
        #Tenant
        #tentat = 0 #LIWC Analysis
        #Differtiation
        #differ = 0 #LIWC Analysis
        #Perceptual processes
        #percept = 0 #LIWC Analysis
        #Verbs past focus VBD VBN
        focuspast = 0
        # focuspast = len(focuspast_list)/wordCount
        focuspast = len([x for x in text if x in LIWC["Past"]])/wordCount * 100
        #Verbs present focus VB VBP VBZ VBG
        focuspresent = 0
        focuspresent = len([x for x in text if x in LIWC["Present"]])/wordCount * 100
        #net speak
        #netspeak = 0 #LIWC Analysis
        #Assent
        #assent = 0 #LIWC Analysis
        #Non fluencies
        #nonflu = 0 #LIWC Analysis

        #return numpy.array([wordCount,readabilityScore,ReadabilityGrade,DirectionCount,Analytic,Authentic,Tone,WPS,Sixltr,function,pronoun,ppron,i,you,ipron,prep,auxverb,negate,interrog,number,cogproc,cause,discrep,tentat,differ,percept,focuspast,focuspresent,netspeak,assent,nonflu,AllPunc,Comma,QMark,Exemplify])
        return [wordCount, readabilityScore, ReadabilityGrade, DirectionCount, WPS, Sixltr, pronoun, ppron, i, you, ipron, prep, verb, auxverb, negate, focuspast, focuspresent, AllPunc, Comma, QMark, Colon, Dash, Parenth, Exemplify]


# In[9]:

# print("here\n")
# xls = xlrd.open_workbook('test_daniela_python.xlsx',"r")
# df1 = xls.sheet_by_name('nppersuasive')
# df2 = xls.sheet_by_name('persuasive')

xls = xlrd.open_workbook('pliwc.xlsx',"r")
pxls = xls.sheet_by_name('pliwc')
textPers = pxls.col_values(1)
result = gettingFeatures(textPers[1])

cols = ['wordCount', 'readabilityScore', 'ReadabilityGrade', 'DirectionCount', 'WPS',
        'Sixltr', 'pronoun', 'ppron', 'i', 'you', 'ipron', 'prep','verb','auxverb', 'negate', 
         'focuspast', 'focuspresent', 'AllPunc', 'Comma', 'QMark', 'Colon','Dash','Parenth','Exemplify']

for i in range(len(result)):
    print(cols[i] + ": " + str(result[i]))
 


