import numpy
import re
import persuasion
from sklearn.externals import joblib
from textstat.textstat import textstat
import nltk
import collections as ct
from nltk import word_tokenize

def textCheck(text, models = None):
    data = numpy.array(persuasion.gettingFeatures(text))
    result = []
    if bool(models):
        for model in models:
            if model == "LogisticRegression":
                loaded_model = joblib.load("models/LogisticRegression.sav")
                predictions = loaded_model.predict(data.reshape(1,-1))
                prob = loaded_model.predict_proba(data.reshape(1,-1))
                result.append((predictions[0], prob, "Logistic Regression"))
            if model == "LinearDiscriminantAnalysis":
                loaded_model = joblib.load("models/LinearDiscriminantAnalysis.sav")
                predictions = loaded_model.predict(data.reshape(1,-1))
                prob = loaded_model.predict_proba(data.reshape(1,-1))
                result.append((predictions[0], prob, "Linear Discriminant Analysis"))
            if model == "KNeighborsClassifier":
                loaded_model = joblib.load("models/KNeighborsClassifier.sav")
                predictions = loaded_model.predict(data.reshape(1,-1))
                prob = loaded_model.predict_proba(data.reshape(1,-1))
                result.append((predictions[0], prob, "KNeighborsClassifier"))
            if model == "DecisionTreeClassifier":
                loaded_model = joblib.load("models/DecisionTreeClassifier.sav")
                predictions = loaded_model.predict(data.reshape(1,-1))
                prob = loaded_model.predict_proba(data.reshape(1,-1))
                result.append((predictions[0], prob, "DecisionTreeClassifier"))
            if model == "GaussianNB":
                loaded_model = joblib.load("models/GaussianNB.sav")
                predictions = loaded_model.predict(data.reshape(1,-1))
                prob = loaded_model.predict_proba(data.reshape(1,-1))
                result.append((predictions[0], prob, "Gaussian Naive Bayes"))
            if model == "RandomForest":
                loaded_model = joblib.load("models/RandomForest.sav")
                predictions = loaded_model.predict(data.reshape(1,-1))
                prob = loaded_model.predict_proba(data.reshape(1,-1))
                result.append((predictions[0], prob, "Random Forest"))
            if model == "SupportVectorMachine":
                loaded_model = joblib.load("models/SupportVectorMachine.sav")
                predictions = loaded_model.predict(data.reshape(1,-1))
                prob = loaded_model.decision_function(data.reshape(1,-1))
                result.append((predictions[0], prob, "Support Vector Machine"))
    print(str(result))
    return result

textCheck("today is a sunny day, let's have some fun!", 
        ["LogisticRegression", "LinearDiscriminantAnalysis", "KNeighborsClassifier",
        "DecisionTreeClassifier", "GaussianNB", "RandomForest", "SupportVectorMachine"])