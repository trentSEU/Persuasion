import nltk
import string
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

path = './tf-idf'
token_dict = {}


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
    return stems

punctuations = ""
for p in string.punctuation:
    punctuations = punctuations + p

for dirpath, dirs, files in os.walk(path):
    for f in files:
        fname = os.path.join(dirpath, f)
        print ("fname=", fname)
        with open(fname) as pearl:
            text = pearl.read()
            intab = punctuations
            outtab = ""
            trantab = str.maketrans(intab, outtab)
            token_dict[f] = text.lower().translate(trantab)

tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values()) #Learn vocabulary and idf, return term-document matrix.

str = 'all great and precious things are lonely.'
response = tfidf.transform([str]) # Uses the vocabulary and document frequencies (df) learned by fit (or fit_transform).
print (response)

feature_names = tfidf.get_feature_names()
for col in response.nonzero()[1]:
    print (feature_names[col], ' - ', response[0, col])