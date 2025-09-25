from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)
print(clf)
print(clf.predict([[2., 2.]]))
print(clf.support_vectors_)
print(clf.support_)
print(clf.n_support_)

data = datasets.load_iris()
X = data.data
Y = data.target
print(data.target_names)

df = pd.DataFrame(X, columns=data.feature_names)
df["species"] = data.target
df["species"] = df["species"].map({0: "setosa", 1: "versicolor", 2: "virginica"})
print(df.head())

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

sns.pairplot(df, hue="species")
plt.show()

svm_linear = SVC(kernel="linear")
svm_linear.fit(X_train, Y_train)
predictions_linear = svm_linear.predict(X_test)
print("Accuracy with linear kernel:", accuracy_score(Y_test, predictions_linear))

svm_rbf = SVC(kernel="rbf")
svm_rbf.fit(X_train, Y_train)
predictions_rbf = svm_rbf.predict(X_test)
print("Accuracy with RBF kernel:", accuracy_score(Y_test, predictions_rbf))
