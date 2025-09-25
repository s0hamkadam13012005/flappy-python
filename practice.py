import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn import datasets

data = datasets.load_iris()
X = data.data
Y = data.target

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3,random_state=1)

model = GaussianNB()
model.fit(x_train,y_train)
prediction = model.predict(x_test)

print("Accuracy : ",accuracy_score(y_test,prediction))
