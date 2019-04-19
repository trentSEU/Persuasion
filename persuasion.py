#!/usr/bin/env python
# coding: utf-8
import numpy as np
import re
import json
import csv
import string
import os
import xlrd
import pandas as pd
import nltk
import collections as ct
import pickle
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from textstat.textstat import textstat
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

# Return a list contains all the given texts
def getTexts(texts):
    translator = str.maketrans('', '', string.punctuation)
    texts = [str(t).lower().translate(translator) for t in texts]
    return texts

# tokenizer for TfidfVectorizer
def tokenize(plainText):
    plainText = plainText.lower()
    punctuation = "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
    for p in punctuation:
        if p != '\'':
            plainText = plainText.replace(p, ' ')

    # '\n' would affect the result -> '\n'i, where i is the first word in a paragraph
    plainText = plainText.replace('\n', ' ')
    plainText = plainText.replace('\t', ' ')
    tokens = plainText.split(" ")
    while tokens.count(''): tokens.remove('')
    lemmas = []
    for item in tokens:
        lemmas.append(wordnet_lemmatizer.lemmatize(item, pos="v"))
    return lemmas

# Generate a vectorizer for tfidf, then dump the vectorizer for future use
# Using getTexts(texts) method to preprocess the corpus then call this frunction to generate the vectorizer
def tfidfVectorizerGenerator(allText):
    tfidfV = TfidfVectorizer(tokenizer=tokenize, stop_words='english', norm=None)
    tfs = tfidfV.fit_transform(allText)
    pickle.dump(tfidfV, open("vectorizer.pickle", "wb"))

def gettingFeatures(plainText):
        plainText = plainText.lower()
        syllables = textstat.syllable_count(plainText)
        sentences = len(sent_tokenize(plainText))
        
        #Count all punctuation
        AllPunc = 0
        punc = "!\',./:;<=>?_`{|}~"
        #"!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
        cd = {c:val for c, val in ct.Counter(plainText).items() if c in punc}
        for x in cd.values():
            AllPunc = AllPunc + x
        
        # Number of commas
        Comma = 0
        Comma = plainText.count(",")
        # Number of question marks
        QMark = 0
        QMark = plainText.count("?")
        # Number of colons
        Colon = 0
        Colon = plainText.count(":")
        # Number of dash
        Dash = 0
        Dash = plainText.count("-")
        # Number of Parenth
        Parenth = 0
        Parenth = plainText.count("(") + plainText.count(")")
        
        # Replace all the punctuations with empty space
        punctuation = "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
        for p in punctuation:
            if p != '\'':
                plainText = plainText.replace(p, ' ')

        # '\n' would affect the result -> '\n'i, where i is the first word in a paragraph
        plainText = plainText.replace('\n', ' ')
        plainText = plainText.replace('\t', ' ')
        text = plainText.split(" ")
        while text.count(''): text.remove('')
        
	    # Total number of words in the text
        wordCount = len(text)
        
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
        DirectionCount  = 0
        DirectionCount = text.count("here") + text.count("there") + plainText.count("over there") + text.count("beyond") + text.count("nearly") + text.count("opposite") + text.count("under") + plainText.count("to the left") + plainText.count("to the right") + plainText.count("in the distance")
        #Exemplify count
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
        pronoun = len([x for x in text if x in LIWC["Pronoun"]])/wordCount * 100
        #Personal pronouns
        ppron = 0
        ppron = len([x for x in text if x in LIWC["Ppron"]])/wordCount * 100
        #I
        feature_i = 0
        feature_i = len([x for x in text if x in LIWC["i"]])/wordCount * 100
        #You
        you = 0
        you = len([x for x in text if x in LIWC["You"]])/wordCount * 100
        #Impersonal pronoun "one" / "it"
        ipron = 0
        # ipron = (text.count("one") + text.count("it"))/wordCount
        ipron = len([x for x in text if x in LIWC["ipron"]])/wordCount * 100
        #Prepositions
        prep = 0
        # prep = len([ (x,y) for x, y in result if y  == "IN" ])/wordCount
        prep = len([x for x in text if x in LIWC["Prep"]])/wordCount * 100
        # Verb
        verb = 0
        verb = len([x for x in text if x in LIWC["Verb"]])/wordCount * 100
        #Auxiliary verbs do/be/have
        auxverb = 0
        auxverb = len([x for x in text if x in LIWC["Auxverb"]])/wordCount * 100
        #Negations
        negate = 0
        negate = len([x for x in text if x in LIWC["Negate"]])/wordCount * 100
        #Count interrogatives
        #interrog = 0 #LICW Analysis
        #Count numbers
        number = 0
        number = len([x for x in text if x in LIWC["Number"]])/wordCount * 100

        #tf-idf
        tfidf = 0
        response = tfidfV.transform([plainText])
        feature_names = tfidfV.get_feature_names()
        for col in response.nonzero()[1]:
            tfidf += response[0, col]
        
        # Transitional words
        transitional_words = 0
        sum_t1 = 0
        sum_t2 = 0

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
            sum_t1 = text.count(i)+ sum_t1
        for i in t2:
            sum_t2 = plainText.count(i)+ sum_t2
        transitional_words = (sum_t1/wordCount) * 100
        transitional_phrases = sum_t2

        # Transitional word1: addition
        sub_sum1 = 0
        sub_sum2 = 0
        addition_1 = ['also', 'again', 'besides', 'furthermore', 'likewise', 'moreover', 'similarly']
        addition_2 = ['as well as', 'coupled with', 'in addition', ]
        for i in  addition_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in addition_2:
            sub_sum2 = plainText.count(i)+ sub_sum2
        addition_words = (sub_sum1/wordCount) * 100
        addition_phrases = sub_sum2
        
        # Transitional word2: consequence
        sub_sum1 = 0
        sub_sum2 = 0
        consequence_1 = ['accordingly', 'consequently', 'hence', 'otherwise', 'subsequently', 'therefore', 'thus', 'thereupon', 'wherefore']
        consequence_2 = ['as a result', 'for this reason', 'for this purpose', 'so then']
        for i in consequence_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in consequence_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        consequence_words = (sub_sum1/wordCount) * 100
        consequence_phrases = sub_sum2
        
        # Transitional word3: contrast_and_Comparison
        sub_sum1 = 0
        sub_sum2 = 0
        contrast_and_Comparison_1 = ['contrast', 'conversely', 'instead', 'likewise', 'rather', 'similarly', 'yet', 'but', 'however', 'still', 'nevertheless']
        contrast_and_Comparison_2 = ['by the same token', 'on one hand', 'on the other hand', 'on the contrary', 'in contrast']
        for i in contrast_and_Comparison_1:
            sub_sum1 = text.count(i)+ sub_sum1  
        for i in contrast_and_Comparison_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        contrast_and_Comparison_words = (sub_sum1/wordCount) * 100
        contrast_and_Comparison_phrases = sub_sum2
        
        # Transitional word4: direction
        sub_sum1 = 0
        sub_sum2 = 0
        direction_1 = ['here', 'there', 'beyond', 'nearly', 'opposite', 'under', 'above']
        direction_2 = ['over there', 'to the left', 'to the right', 'in the distance']
        for i in direction_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in direction_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        direction_words = (sub_sum1/wordCount) * 100
        direction_phrases = sub_sum2

        # Transitional word5: diversion
        sub_sum1 = 0
        sub_sum2 = 0
        diversion_1 = ['incidentally']
        diversion_2 = ['by the way']
        for i in diversion_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in diversion_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        diversion_words = (sub_sum1/wordCount) * 100
        diversion_phrases = sub_sum2

        # Transitional word6: emphasis
        sub_sum1 = 0
        sub_sum2 = 0
        emphasis_1 = ['chiefly', 'especially', 'particularly', 'singularly']
        emphasis_2 = ['above all', 'with attention to']
        for i in emphasis_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in emphasis_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        emphasis_words = (sub_sum1/wordCount) * 100 
        emphasis_phrases = sub_sum2  

        # Transitional word7: exception
        sub_sum1 = 0
        sub_sum2 = 0
        exception_1 = ['barring', 'beside', 'except', 'excepting', 'excluding', 'save']
        exception_2 = ['aside from', 'exclusive of', 'other than', 'outside of']
        for i in exception_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in exception_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        exception_words = (sub_sum1/wordCount) * 100 
        exception_phrases = sub_sum2    

        # Transitional word8: exemplifying
        sub_sum1 = 0
        sub_sum2 = 0
        exemplifying_1 = ['chiefly', 'especially', 'markedly', 'namely', 'particularly', 'including' , 'specifically']
        exemplifying_2 = ['for instance', 'in particular', 'such as']
        for i in exemplifying_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in exemplifying_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        exemplifying_words = (sub_sum1/wordCount) * 100 
        exemplifying_phrases = sub_sum2 

        # Transitional word9: generalizing
        sub_sum1 = 0
        sub_sum2 = 0
        generalizing_1 = ['generally', 'ordinarily', 'usually']
        generalizing_2 = ['as a rule', 'as usual', 'for the most part', 'generally speaking']
        for i in generalizing_1:
            sub_sum1 = text.count(i)+ sub_sum1 
        for i in generalizing_2:
            sub_sum2 = plainText.count(i)+ sub_sum2
        generalizing_words = (sub_sum1/wordCount) * 100
        generalizing_phrases = sub_sum2

        # Transitional word10: illustration
        sub_sum1 = 0
        sub_sum2 = 0
        illustration_1 = []
        illustration_2 = ['for example', 'for instance', 'for one thing', 'as an illustration', 'illustrated with', 'as an example', 'in this case']
        for i in illustration_1:
            sub_sum1 = text.count(i)+ sub_sum1
        for i in illustration_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        illustration_words = (sub_sum1/wordCount) * 100 
        illustration_phrases = sub_sum2

        # Transitional word11: similarity
        sub_sum1 = 0
        sub_sum2 = 0
        similarity_1 = ['comparatively', 'correspondingly', 'identically', 'likewise', 'similar', 'moreover']
        similarity_2 = ['coupled with', 'together with']
        for i in similarity_1:
            sub_sum1 = text.count(i)+ sub_sum1
        for i in similarity_2:
            sub_sum2 = plainText.count(i)+ sub_sum2
        similarity_words = (sub_sum1/wordCount) * 100 
        similarity_phrases = sub_sum2

        # Ransitional word12: restatement
        sub_sum1 = 0
        sub_sum2 = 0
        restatement_1 = ['namely']
        restatement_2 = ['in essence', 'in other words', 'that is', 'that is to say', 'in short', 'in brief', 'to put it differently']
        for i in restatement_1:
            sub_sum1 = text.count(i)+ sub_sum1
        for i in restatement_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        restatement_words = (sub_sum1/wordCount) * 100 
        restatement_phrases = sub_sum2

        # Transitional word13: sequence
        sub_sum1 = 0
        sub_sum2 = 0
        sequence_1 = ['next', 'then', 'soon', 'later', 'while', 'earlier','simultaneously', 'afterward']
        sequence_2 = ['at first', 'first of all', 'to begin with', 'in the first place', 'at the same time', 'for now', 'for the time being'
        , 'the next step', 'in time', 'in turn', 'later on', 'the meantime', 'in conclusion', 'with this in mind']
        for i in sequence_1:
            sub_sum1 = text.count(i)+ sub_sum1
        for i in sequence_2:
            sub_sum2 = plainText.count(i)+ sub_sum2
        sequence_words = (sub_sum1/wordCount) * 100
        sequence_phrases = sub_sum2
        

        # Transitional word14: summarizing
        sub_sum1 = 0
        sub_sum2 = 0
        summarizing_1 = ['briefly', 'finally']
        summarizing_2 = [ 'after all', 'all in all', 'all things considered', 'by and large', 'in any case', 'in any event'
        , 'in brief', 'in conclusion', 'on the whole', 'in short', 'in summary', 'in the final analysis', 'in the long run', 'on balance'
        , 'to sum up', 'to summarize']
        for i in summarizing_1:
            sub_sum1 = text.count(i)+ sub_sum1
        for i in summarizing_2:
            sub_sum2 = plainText.count(i)+ sub_sum2 
        summarizing_words = (sub_sum1/wordCount) * 100    
        summarizing_phrases = sub_sum2    
        
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

        return [wordCount, readabilityScore, ReadabilityGrade, DirectionCount, WPS, Sixltr, pronoun, ppron, feature_i, you
        , ipron, prep, verb, auxverb, negate, focuspast, focuspresent, AllPunc, Comma, QMark, Colon, Dash, Parenth
        , Exemplify, tfidf, transitional_words, transitional_phrases, addition_words, addition_phrases, consequence_words, consequence_phrases
        , contrast_and_Comparison_words, contrast_and_Comparison_phrases, direction_words, direction_phrases, diversion_words, diversion_phrases
        , emphasis_words, emphasis_phrases, exception_words, exception_phrases, exemplifying_words, exemplifying_phrases, generalizing_words, generalizing_phrases
        , illustration_words, illustration_phrases, similarity_words, similarity_phrases
        , restatement_words, restatement_phrases, sequence_words, sequence_phrases,summarizing_words,summarizing_phrases]

LIWC_JSON = open("LIWC2015_Lower_i.json",'r')
LIWC = json.load(LIWC_JSON)
tfidfV = pickle.load(open("vectorizer.pickle", "rb")) # Vectorizer used for TfIdf calculation

xls = xlrd.open_workbook('test_daniela_python.xlsx',"r")
xls = xlrd.open_workbook('test_daniela_python.xlsx',"r")
df1 = xls.sheet_by_name('nppersuasive')
df2 = xls.sheet_by_name('persuasive')

textNPers = df1.col_values(0)[1:]
textPers = df2.col_values(0)[1:]

alltexts = textNPers[:]
alltexts.extend(textPers)
ALLTEXTS = getTexts(alltexts)

# Feature names
cols = ['text', 'wordCount', 'readabilityScore', 'ReadabilityGrade', 'DirectionCount', 'WPS' ,'Sixltr', 'pronoun', 'ppron'
        , 'i', 'you', 'ipron', 'prep','verb','auxverb', 'negate','focuspast', 'focuspresent', 'AllPunc', 'Comma'
        , 'QMark', 'Colon','Dash','Parenth','Exemplify', 'tfidf', 'transitional_words', 'transitional_phrases', 'addition_words'
        , 'addition_phrases', 'consequence_words', 'consequence_phrases', 'contrast_and_Comparison_words'
        , 'contrast_and_Comparison_phrases', 'direction_words', 'direction_phrases', 'diversion_words', 'diversion_phrases'
        , 'emphasis_words', 'emphasis_phrases', 'exception_words', 'exception_phrases', 'exemplifying_words'
        , 'exemplifying_phrases', 'generalizing_words', 'generalizing_phrases', 'illustration_words'
        , 'illustration_phrases', 'similarity_words', 'similarity_phrases', 'restatement_words'
        , 'restatement_phrases', 'sequence_words', 'sequence_phrases','summarizing_words','summarizing_phrases', 'persuasion']

# Getting the given texts' features and save in a csv file
count_item = 1
with open('P_NP_Output.csv', mode='w') as csvfile:
    csvfile.write(','.join(cols))
    for t in textNPers:
        rowList = [""] * len(cols)
        features = gettingFeatures(str(t))
        for i in range(len(features)):
            rowList[i + 1] = str(features[i])
        text = str(t).replace("\"", "\"\"")
        text = "\"" + text + "\""
        rowList[0] = text
        rowList[len(cols) - 1] = "0" # 0 for non-persuasive
        csvfile.write("\n" + ','.join(rowList))
        if count_item % 20 == 0:
            print(count_item)
        count_item += 1
    for t in textPers:
        rowList = [""] * len(cols)
        features = gettingFeatures(str(t))
        for i in range(len(features)):
            rowList[i + 1] = str(features[i])
        text = str(t).replace("\"", "\"\"")
        text = "\"" + text + "\""
        rowList[0] = text
        rowList[len(cols) - 1] = "1" # 1 for non-persuasive
        csvfile.write("\n" + ','.join(rowList))
        if count_item % 20 == 0:
            print(count_item)
        count_item += 1