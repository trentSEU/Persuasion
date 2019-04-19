import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy
print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas
print('pandas: {}'.format(pandas.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))


from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.utils import shuffle
from sklearn.externals import joblib
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier

url = "P_NP_Input.csv"
dataset = pandas.read_csv(url)
dataset.apply(pandas.to_numeric)

# shape
print(dataset.shape)

#Shuffle the dataset
df = shuffle(dataset)

# head
# print(df.head(20))

#set training and testing dataset (70-30)
array = df.values
X = array[:,0:55]
Y = array[:,55]
print(len(X[0]))
validation_size = 0.30
seed = 7
scoring = 'accuracy'
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
models.append(('RF',RandomForestClassifier()))
# evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = model_selection.KFold(n_splits=4, random_state=None) # split data into k consecutive folds, each time, one used as test set, k - 1 used as training set
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring='f1_weighted') # cv: the number of sets of cross_validation
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

# Compare Algorithms
# fig = plt.figure()
# fig.suptitle('Algorithm Comparison')
# ax = fig.add_subplot(111)
# plt.boxplot(results)
# ax.set_xticklabels(names)
# plt.show()

# Make predictions on validation dataset
print("Support Vector Machine")
svm = SVC()
svm.fit(X_train, Y_train)
predictions = svm.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#Save the model
filename = 'models/SupportVectorMachine.sav'
joblib.dump(svm, filename)

# Make predictions on validation dataset
print("Logistic Regression")
lr = LogisticRegression()
lr.fit(X_train, Y_train)
predictions = lr.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#Save the model
filename = 'models/LogisticRegression.sav'
joblib.dump(lr, filename)

# Make predictions on validation dataset
print("Linear Discriminant Analysis")
ld = LinearDiscriminantAnalysis()
ld.fit(X_train, Y_train)
predictions = ld.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#Save the model
filename = 'models/LinearDiscriminantAnalysis.sav'
joblib.dump(ld, filename)

# Make predictions on validation dataset
print("KNeighborsClassifier")
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
predictions = knn.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#Save the model
filename = 'models/KNeighborsClassifier.sav'
joblib.dump(knn, filename)

# Make predictions on validation dataset
print("DecisionTreeClassifier")
dt = DecisionTreeClassifier()
dt.fit(X_train, Y_train)
predictions = dt.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#Save the model
filename = 'models/DecisionTreeClassifier.sav'
joblib.dump(dt, filename)

# Make predictions on validation dataset
print("GaussianNB")
nb = GaussianNB()
nb.fit(X_train, Y_train)
predictions = nb.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#Save the model
filename = 'models/GaussianNB.sav'
joblib.dump(nb, filename)

# Make predictions on validation dataset
print("Random Forest")
rf = RandomForestClassifier()
rf.fit(X_train, Y_train)
predictions = rf.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#Save the model
filename = 'models/RandomForest.sav'
joblib.dump(rf, filename)

print("finished")


"""
#Saving the best model Gausian 
model = KNeighborsClassifier()
model.fit(X_train, Y_train)
# save the model to disk
#filename = 'KNeighborsClassifier.sav'
#joblib.dump(model, filename)

#Loading and testing the best model
filename = 'KNeighborsClassifier.sav'
loaded_model = joblib.load(filename)
result = loaded_model.score(X_validation, Y_validation)
print(result)
loaded_model.precision_recall_fscore_support(X_validation, Y_validation, average='macro')
"""