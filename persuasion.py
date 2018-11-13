#!/usr/bin/env python
# coding: utf-8
import numpy as np
import re
from sklearn.externals import joblib
from textstat.textstat import textstat
import nltk
import collections as ct
from nltk import word_tokenize
import xlrd
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
import json
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


# In[4]:

LIWC_JSON =  open("LIWC.json",'r')
LIWC = json.load(LIWC_JSON)

def gettingFeatures(plainText):
        plainText = plainText.lower()
        syllables = textstat.syllable_count(plainText)
        sentences = textstat.sentence_count(plainText)
        
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
        Parenth = plainText.count("'")
        
        #Short version to full words
        mapping = [('can\'t', 'can not'), ('let\'s', 'let us'), ('isn\'t', 'is not'), ('i\'m', 'i am'), 
                   ('don\'t', 'do not'), ('doesn\'t', 'does not'), ('that\'s' , 'that is'), ('i\'s' , 'it is'), 
                   ('i\'ve' , 'i have'), ('wouldn\'t', 'would not'), ('it\'s', 'it is'), ('he\'s', 'he is')] 
        for (k, v) in mapping:
            plainText = plainText.replace(k, v)
        
        # replace all the punctuations with empty space
        punctuation = "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
        for p in punctuation:
            if p != '\'':
                plainText = plainText.replace(p, ' ')

        # text is the list version of plainText
     

#         for i in range(len(apostrophe)):
#             strr=paste("***",i,"***")
#             text = re.replace(apostrophe[i],strr,text)


#         for i in range(len(apostrophe)):
#             strr=paste("***",i,"***")
#             text = re.replace(strr, apostrophe[i], text)
        text = plainText.split(" ")
        while text.count(''): text.remove('')
#         print(str(text))

        wordsWithNumbers = []
        # check all the words
        for word in text:
            # check the current word
            for character in word:
                if character.isdigit():
                    wordsWithNumbers.append(word)
                    break

        return wordsWithNumbers
        
	#words / syllables / sentences count
        wordCount = len(plainText.split()) 
        
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
        DiractionCount  = 0
        DiractionCount = text.count("here") + text.count("there") + plainText.count("over there") + text.count("beyond") + text.count("nearly") + text.count("opposite") + text.count("under") + plainText.count("to the left") + plainText.count("to the right") + plainText.count("in the distance")
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
            parts = [len(l.split()) for l in re.split(r'[?!.]', plainText) if l.strip()]
            WPS = sum(parts)/len(parts) #number of words per sentence
        except:
            WPS = 0
        #Six letter words
        Sixltr = 0
        words = plainText.split()
        letter_count_per_word = {w:len(w) for w in words}
        for x in letter_count_per_word.values():
            if x >= 6:
                Sixltr = Sixltr + 1
        #Function words
        function = 0
        #Pronouns
        pronoun = 0
        text_tokens = word_tokenize(plainText)
        result = nltk.pos_tag(text_tokens)
        pronoun = len([ (x,y) for x, y in result if y  == "PRP" or y  == "PRP$"])/wordCount
        #Personal pronouns
        ppron = 0
        ppron = len([ (x,y) for x, y in result if y  == "PRP" ])/wordCount
        #I
        i = 0
        i = text.count("i")/wordCount
        #You
        you = 0
        you = text.count("you")/wordCount
        #Impersonal pronoun "one" / "it"
        ipron = 0
        ipron = (text.count("one") + text.count("it"))/wordCount
        #Prepositions
        prep = 0
        prep = len([ (x,y) for x, y in result if y  == "IN" ])/wordCount
        #Verb
        verb = 0
        text_tokens = word_tokenize(plainText)
        result = nltk.pos_tag(text_tokens)
        verb = len([ (x,y) for x, y in result if y  == "VB" or y  == "VBD" or y  == "VBG" 
                       or y  == "VBN" or y  == "VBP" or y  == "VBZ"])/wordCount
        #Auxiliary verbs do/be/have
        auxverb = 0
        auxverb = (text.count("do") + text.count("does") + text.count("don´t") + text.count("doesn´t") + text.count("has") + text.count("have") + text.count("hasn´t")+ text.count("haven´t") + text.count("am") + text.count("are") +  text.count("is") + plainText.count("´m") + plainText.count("´re") +  plainText.count("´s"))/wordCount
        #Negations
        negate = 0
        negate = text.count("not")/wordCount
        #Count interrogatives
        #interrog = 0 #LICW Analysis
        #Count numbers
        number = 0
        
        prep = len([ (x,y) for x, y in result if y  == "CD" ])/wordCount
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
        focuspast_list = []
        LIWC_focus_past = LIWC["Past"]
        for word in text:
            if word in LIWC_focus_past:
                focuspast_list.append(word)
        focuspast = len(focuspast_list)/wordCount
        #Verbs present focus VB VBP VBZ VBG
        focuspresent = 0
        focuspresent_list = []
        LIWC_focus_present = LIWC["Present"]
        for word in text:
            if word in LIWC_focus_present:
                focuspresent_list.append(word)
        focuspresent = len(focuspresent_list)/wordCount
        #net speak
        #netspeak = 0 #LIWC Analysis
        #Assent
        #assent = 0 #LIWC Analysis
        #Non fluencies
        #nonflu = 0 #LIWC Analysis

        #return numpy.array([wordCount,readabilityScore,ReadabilityGrade,DiractionCount,Analytic,Authentic,Tone,WPS,Sixltr,function,pronoun,ppron,i,you,ipron,prep,auxverb,negate,interrog,number,cogproc,cause,discrep,tentat,differ,percept,focuspast,focuspresent,netspeak,assent,nonflu,AllPunc,Comma,QMark,Exemplify])
        return [wordCount, readabilityScore, ReadabilityGrade, DiractionCount, WPS, Sixltr, pronoun, ppron, i, you, ipron, prep, verb, auxverb, negate, focuspast, focuspresent, AllPunc, Comma, QMark, Colon, Dash, Parenth, Exemplify]


# In[9]:

# print("here\n")
xls = xlrd.open_workbook('test_daniela_python.xlsx',"r")
df1 = xls.sheet_by_name('nppersuasive')
df2 = xls.sheet_by_name('persuasive')


# In[6]:


cols = ['wordCount', 'readabilityScore', 'ReadabilityGrade', 'DiractionCount', 'WPS',
        'Sixltr', 'pronoun', 'ppron', 'i', 'you', 'ipron', 'prep','verb','auxverb', 'negate', 
         'focuspast', 'focuspresent', 'AllPunc', 'Comma', 'QMark', 'Colon','Dash','Parenth','Exemplify']


# text1 = df1.col_values(0)
# text1 = text1[1:]
# plainText = text1[1]
# plainText = plainText.lower()
# mapping = [ ('can\'t', 'can not'), ('let\'s', 'let us'), ('isn\'t', 'is not'), ('i\'m', 'i am'), ('don\'t', 'do not'),
#                   ('that\'s' , 'that is')] 
# for (k, v) in mapping:
#     plainText = plainText.replace(k, v)
# #Count all punctuation
# AllPunc = 0
# punctuation = "!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~" ###need to take out some
# cd = {c:val for c, val in ct.Counter(plainText).items() if c in punctuation}
# for x in cd.values():
#     AllPunc = AllPunc + x
# #number of commas
# Comma = 0
# Comma = plainText.count(",")
# #number of question marks
# QMark = 0
# QMark = plainText.count("?")
# 
# for p in punctuation:
#     if p != '\'':
#         plainText = plainText.replace(p, ' ')
# 
# # text is the list version of plainText
# text = plainText.split(" ")
# text

# In[10]:


# textP = df1.col_values(0)
# textP = textP[1:]
# wordsWithNumbers = []
# for text in textP:
#     wordsWithNumbers.extend(gettingFeatures(text))

# for word in wordsWithNumbers:
#     for character in word:
#         if not character.isdigit():
#             print(word)
#             break

# for word in wordsWithNumbers:
#     if '\'' in word:
#         print(word + " ")

# for word in wordsWithNumbers:
#     if 'lbs' in word:
#         print(word + " ")

# In[16]:

# print(wrodsContainsNumber)


# punctuation = '''!#$%&()*+,-./:;<=>?@[\\]^_`{|}~'''
# df = []
# apostrophe = set()
# text = []
# 
# for i in text1:
#     for p in punctuation:
#         i = i.replace(p, ' ')
# 
#     # text is the list version of plainText
#     text.extend(i.split(" "))
# 
# for j in text:
#     if ('\'s' in j or 's\'' in j) and j.count('\'') == 1:
#         apostrophe.add(j)
#         
# print((apostrophe))
# 
# 

# text2 = df2.col_values(0)
# text2 = text2[1:]

# punctuation = '''!#$%&()*+,-./:;<=>?@[\\]^_`{|}~'''
# apostrophe2 = set()
# text_2 = []
# 
# for i in text2:
#     for p in punctuation:
#         i = str(i).replace(p, ' ')
# 
#     # text is the list version of plainText
#     text_2.extend(i.split(" "))
# for j in text_2:
#     if ('\'s' in j or 's\'' in j) and j.count('\'') == 1:
#         apostrophe2.add(j)
# 
#         
# print((apostrophe2))

# In[9]:


# df_np=pd.DataFrame(df_np).T
# df_np=pd.DataFrame(df_np).T
# df_np.columns = cols
# df_np


# # In[10]:


# text2 = df2.col_values(0)
# text2 = text2[1:]
# df_p = []
# for text in text2:
#     df_p.append(gettingFeatures(str(text)))


# # In[13]:


# df_p=pd.DataFrame(df_p).T
# df_p=pd.DataFrame(df_p).T
# df_p.columns = cols
# df_p


# # In[111]:


# #df_2


# # In[58]:


# writer = pd.ExcelWriter('output_1101.xlsx', engine='xlsxwriter')

# # Convert the dataframe to an XlsxWriter Excel object.
# df_np.to_excel(writer, sheet_name='npper', index =False ,header=True)
# df_p.to_excel(writer, sheet_name='pper', index =False ,header=True)
# # Close the Pandas Excel writer and output the Excel file.

# writer.save()


# In[ ]:




