# Ensemble Voting Classifier (Logistic Regression, Decision Tree, SVM)

import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
names = ['preg','plas','pres','skin','test','mass','pedi','age','class']
df = pd.read_csv(url, names=names)

array = df.values
X = array[:,0:8]
Y = array[:,8]
seed = 7

estimators = []

model1 = Pipeline([
    ('scaler', StandardScaler()),
    ('Logistic', LogisticRegression(max_iter=200))
])
estimators.append(('Logistic', model1))

model2 = DecisionTreeClassifier()
estimators.append(('CART', model2))

model3 = Pipeline([
    ('scaler', StandardScaler()),
    ('SVM', SVC())
])
estimators.append(('SVM', model3))

ensemble = VotingClassifier(estimators=estimators)

kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
results = model_selection.cross_val_score(ensemble, X, Y, cv=kfold)

print("Mean Accuracy: %.3f" % results.mean())
print("Standard Deviation: %.3f" % results.std())
