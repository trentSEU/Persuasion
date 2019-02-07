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

LIWC_JSON =  open("LIWC2015_Lower_i.json",'r')
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

        # '\n' would affect the result -> '\n'i, where i is the first word in a paragraph
        plainText = plainText.replace('\n', ' ')
        plainText = plainText.replace('\t', ' ')
        text = plainText.split(" ")
        while text.count(''): text.remove('')
        
	#words / syllables / sentences count
        wordCount = len(text)
        # wordCount = 1743
        
        try:
            #ReadabilityScore
            readabilityScore = 206.835 - 1.015 * (wordCount / sentences) - 84.6 * (syllables / wordCount)
            #ReadabilityGrade
            ReadabilityGrade = 0.39 * (wordCount / sentences) + 11.8 * (syllables / wordCount) - 15.59
        except:
            readabilityScore = 0
            ReadabilityGrade = 0
        #Punctuations
        AllPunc = AllPunc / wordCount * 100
        Comma = Comma / wordCount * 100
        QMark  =QMark / wordCount * 100
        Colon = Colon / wordCount * 100
        Dash = Dash / wordCount * 100
        Parenth = Parenth / wordCount * 100
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
        # pronoun = len([ (x,y) for x, y in result if y  == "PRP" or y  == "PRP$"])/wordCount
        pronoun = len([x for x in text if x in LIWC["Pronoun"]])/wordCount * 100
        #Personal pronouns
        ppron = 0
        # ppron = len([ (x,y) for x, y in result if y  == "PRP" ])/wordCount
        ppron = len([x for x in text if x in LIWC["Ppron"]])/wordCount * 100
        #I
        i = 0
        i = len([x for x in text if x in LIWC["i"]])/wordCount * 100
        #You
        you = 0
        you = len([x for x in text if x in LIWC["You"]])/wordCount * 100
        print([x for x in text if x in LIWC["You"]])
        print()
        #Impersonal pronoun "one" / "it"
        ipron = 0
        # ipron = (text.count("one") + text.count("it"))/wordCount
        ipron = len([x for x in text if x in LIWC["ipron"]])/wordCount * 100
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
        verb = len([x for x in text if x in LIWC["Verb"]])/wordCount * 100
        #Auxiliary verbs do/be/have
        auxverb = 0
        # auxverb = (text.count("do") + text.count("does") + text.count("don´t") + text.count("doesn´t") + text.count("has") + text.count("have") + text.count("hasn´t")+ text.count("haven´t") + text.count("am") + text.count("are") +  text.count("is") + plainText.count("´m") + plainText.count("´re") +  plainText.count("´s"))/wordCount
        auxverb = len([x for x in text if x in LIWC["Auxverb"]])/wordCount * 100
        #Negations
        negate = 0
        # negate = text.count("not")/wordCount
        negate = len([x for x in text if x in LIWC["Negate"]])/wordCount * 100
        #Count interrogatives
        #interrog = 0 #LICW Analysis
        #Count numbers
        number = 0
        number = len([x for x in text if x in LIWC["Number"]])/wordCount * 100
        
        ## transitional words
        transitional_words = 0
        sum_t = 0

        t1 = ['also', 'again', 'besides', 'furthermore', 'likewise', 'moreover', 'similarly','accordingly', 'consequently', 'hence', 'otherwise'
        , 'subsequently', 'therefore', 'thus', 'thereupon', 'wherefore','contrast', 'conversely', 'instead', 'likewise', 'rather', 'similarly'
        , 'yet', 'but', 'however', 'still', 'nevertheless','here', 'there', 'beyond', 'nearly', 'opposite', 'under', 'above','incidentally'
        ,'chiefly', 'especially', 'particularly', 'singularly','barring', 'beside', 'except', 'excepting', 'excluding', 'save','chiefly', 'especially'
        , 'markedly', 'namely', 'particularly', 'including' , 'specifically','generally', 'ordinarily', 'usually','comparatively', 'correspondingly'
        , 'identically', 'likewise', 'similar', 'moreover','namely','next', 'then', 'soon', 'later', 'while', 'earlier','simultaneously', 'afterward'
        ,'briefly', 'finally']

        t2 = ['as well as', 'coupled with', 'in addition', 'as a result', 'for this reason', 'for this purpose', 'so then','by the same token', 'on one hand'
        , 'on the other hand', 'on the contrary', 'in contrast', 'over there', 'to the left', 'to the right', 'in the distance','by the way','above all'
        , 'with attention to','aside from', 'exclusive of', 'other than', 'outside of','for instance', 'in particular', 'such as','as a rule', 'as usual'
        , 'for the most part', 'generally speaking','for example', 'for instance', 'for one thing', 'as an illustration', 'illustrated with', 'as an example'
        , 'in this case','comparatively', 'correspondingly', 'identically', 'likewise', 'similar', 'moreover','in essence', 'in other words', 'that is'
        , 'that is to say', 'in short', 'in brief', 'to put it differently','at first', 'first of all', 'to begin with', 'in the first place'
        , 'at the same time', 'for now', 'for the time being', 'the next step', 'in time', 'in turn', 'later on', 'the meantime', 'in conclusion'
        , 'with this in mind', 'after all', 'all in all', 'all things considered', 'by and large', 'in any case', 'in any event', 'in brief'
        , 'in conclusion', 'on the whole', 'in short', 'in summary', 'in the final analysis', 'in the long run', 'on balance', 'to sum up', 'to summarize']
        
        for i in t1:
            sum_t = text.count(i)+ sum_t
        for i in t2:
            sum_t = plainText.count(i)+ sum_t
        transitional_words = (sum_t/wordCount) * 100

        #transitional word1: addition
        sub_sum = 0
        addition_1 = ['also', 'again', 'besides', 'furthermore', 'likewise', 'moreover', 'similarly']
        addition_2 = ['as well as', 'coupled with', 'in addition', ]
        for i in  addition_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in addition_2:
            sub_sum = plainText.count(i)+ sub_sum 
        addition = (sub_sum/wordCount) * 100

        ##transitional word2: consequence
        sub_sum = 0
        consequence_1 = ['accordingly', 'consequently', 'hence', 'otherwise', 'subsequently', 'therefore', 'thus', 'thereupon', 'wherefore']
        consequence_2 = ['as a result', 'for this reason', 'for this purpose', 'so then']
        for i in consequence_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in consequence_2:
            sub_sum = plainText.count(i)+ sub_sum 
        consequence = (sub_sum/wordCount) * 100
        
        ##transitional word3: contrast_and_Comparison
        sub_sum = 0
        contrast_and_Comparison_1 = ['contrast', 'conversely', 'instead', 'likewise', 'rather', 'similarly', 'yet', 'but', 'however', 'still', 'nevertheless']
        contrast_and_Comparison_2 = ['by the same token', 'on one hand', 'on the other hand', 'on the contrary', 'in contrast']
        for i in contrast_and_Comparison_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in contrast_and_Comparison_2:
            sub_sum = plainText.count(i)+ sub_sum 
        contrast_and_Comparison = (sub_sum/wordCount) * 100
        
        ##transitional word4: direction
        sub_sum = 0
        direction_1 = ['here', 'there', 'beyond', 'nearly', 'opposite', 'under', 'above']
        direction_2 = ['over there', 'to the left', 'to the right', 'in the distance']
        for i in direction_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in direction_2:
            sub_sum = plainText.count(i)+ sub_sum 
        direction = (sub_sum/wordCount) * 100

        ##transitional word5: diversion
        sub_sum = 0
        diversion_1 = ['incidentally']
        diversion_2 = ['by the way']
        for i in diversion_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in diversion_2:
            sub_sum = plainText.count(i)+ sub_sum 
        diversion = (sub_sum/wordCount) * 100

        ##transitional word6: emphasis
        sub_sum = 0
        emphasis_1 = ['chiefly', 'especially', 'particularly', 'singularly']
        emphasis_2 = ['above all', 'with attention to']
        for i in emphasis_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in emphasis_2:
            sub_sum = plainText.count(i)+ sub_sum 
        emphasis = (sub_sum/wordCount) * 100   

        ##transitional word7: exception
        sub_sum = 0
        exception_1 = ['barring', 'beside', 'except', 'excepting', 'excluding', 'save']
        exception_2 = ['aside from', 'exclusive of', 'other than', 'outside of']
        for i in exception_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in exception_2:
            sub_sum = plainText.count(i)+ sub_sum 
        exception = (sub_sum/wordCount) * 100     

        ##transitional word8: exemplifying
        sub_sum = 0
        exemplifying_1 = ['chiefly', 'especially', 'markedly', 'namely', 'particularly', 'including' , 'specifically']
        exemplifying_2 = ['for instance', 'in particular', 'such as']
        for i in exemplifying_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in exemplifying_2:
            sub_sum = plainText.count(i)+ sub_sum 
        exemplifying = (sub_sum/wordCount) * 100  


        ##transitional word9: generalizing
        sub_sum = 0
        generalizing_1 = ['generally', 'ordinarily', 'usually']
        generalizing_2 = ['as a rule', 'as usual', 'for the most part', 'generally speaking']
        for i in generalizing_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in generalizing_2:
            sub_sum = plainText.count(i)+ sub_sum 
        generalizing = (sub_sum/wordCount) * 100

        ##transitional word10: illustration
        sub_sum = 0
        illustration_1 = []
        illustration_2 = ['for example', 'for instance', 'for one thing', 'as an illustration', 'illustrated with', 'as an example', 'in this case']
        for i in illustration_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in illustration_2:
            sub_sum = plainText.count(i)+ sub_sum 
        illustration = (sub_sum/wordCount) * 100 

        ##transitional word11: similarity
        sub_sum = 0
        similarity_1 = ['comparatively', 'correspondingly', 'identically', 'likewise', 'similar', 'moreover']
        similarity_2 = ['coupled with', 'together with']
        for i in similarity_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in similarity_2:
            sub_sum = plainText.count(i)+ sub_sum 
        similarity = (sub_sum/wordCount) * 100 

        ##transitional word12: restatement
        sub_sum = 0
        restatement_1 = ['namely']
        restatement_2 = ['in essence', 'in other words', 'that is', 'that is to say', 'in short', 'in brief', 'to put it differently']
        for i in restatement_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in restatement_2:
            sub_sum = plainText.count(i)+ sub_sum 
        restatement = (sub_sum/wordCount) * 100 

        ##transitional word13: sequence
        sub_sum = 0
        sequence_1 = ['next', 'then', 'soon', 'later', 'while', 'earlier','simultaneously', 'afterward']
        sequence_2 = ['at first', 'first of all', 'to begin with', 'in the first place', 'at the same time', 'for now', 'for the time being'
        , 'the next step', 'in time', 'in turn', 'later on', 'the meantime', 'in conclusion', 'with this in mind']
        for i in sequence_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in sequence_2:
            sub_sum = plainText.count(i)+ sub_sum 
        sequence = (sub_sum/wordCount) * 100

        ##transitional word14: summarizing
        sub_sum = 0
        summarizing_1 = ['briefly', 'finally']
        summarizing_2 = [ 'after all', 'all in all', 'all things considered', 'by and large', 'in any case', 'in any event'
        , 'in brief', 'in conclusion', 'on the whole', 'in short', 'in summary', 'in the final analysis', 'in the long run', 'on balance'
        , 'to sum up', 'to summarize']
        for i in summarizing_1:
            sub_sum = text.count(i)+ sub_sum 
        for i in summarizing_2:
            sub_sum = plainText.count(i)+ sub_sum 
        summarizing = (sub_sum/wordCount) * 100       
        
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
        focuspast = len([x for x in text if x in LIWC["FocusPast"]])/wordCount * 100
        #Verbs present focus VB VBP VBZ VBG
        focuspresent = 0
        focuspresent = len([x for x in text if x in LIWC["FocusPresent"]])/wordCount * 100
        #net speak
        #netspeak = 0 #LIWC Analysis
        #Assent
        #assent = 0 #LIWC Analysis
        #Non fluencies
        #nonflu = 0 #LIWC Analysis

        #return numpy.array([wordCount,readabilityScore,ReadabilityGrade,DirectionCount,Analytic,Authentic,Tone,WPS,Sixltr,function,pronoun,ppron,i,you,ipron,prep,auxverb,negate,interrog,number,cogproc,cause,discrep,tentat,differ,percept,focuspast,focuspresent,netspeak,assent,nonflu,AllPunc,Comma,QMark,Exemplify])
        return [wordCount, readabilityScore, ReadabilityGrade, DirectionCount, WPS, Sixltr, pronoun, ppron, i, you
        , ipron, prep, verb, auxverb, negate, focuspast, focuspresent, AllPunc, Comma, QMark, Colon, Dash, Parenth
        , Exemplify, transitional_words, addition, consequence, contrast_and_Comparison, direction, diversion, emphasis, exception, exemplifying
        , generalizing, illustration, similarity, restatement, sequence, summarizing]


# In[9]:

xls = xlrd.open_workbook('test_daniela_python.xlsx',"r")
df1 = xls.sheet_by_name('nppersuasive')
df2 = xls.sheet_by_name('persuasive')

xls = xlrd.open_workbook('pliwc.xlsx',"r")
pxls = xls.sheet_by_name('pliwc')
textPers = pxls.col_values(1)
result = gettingFeatures(textPers[110])
print(result)
cols = ['wordCount', 'readabilityScore', 'ReadabilityGrade', 'DirectionCount', 'WPS' ,'Sixltr', 'pronoun', 'ppron'
        , 'i', 'you', 'ipron', 'prep','verb','auxverb', 'negate','focuspast', 'focuspresent', 'AllPunc', 'Comma'
        , 'QMark', 'Colon','Dash','Parenth','Exemplify', 'transitional_words','addition', 'consequence', 'contrast_and_Comparison', 'direction', 'diversion', 'emphasis', 'exception', 'exemplifying'
        ,'generalizing', 'illustration', 'similarity', 'restatement', 'sequence', 'summarizing']

for i in range(len(result)):
    print(cols[i] + ": " + str(result[i]))