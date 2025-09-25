import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# ⿡ Load the Iris dataset
iris = load_iris()
X = iris.data[:, :2]  # use only first two features for easy plotting
y = iris.target
class_names = iris.target_names

# ⿢ Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ⿣ Train Gaussian Naive Bayes model
model = GaussianNB()
model.fit(X_train, y_train)

# ⿤ Predict on test set
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# ⿥ Create meshgrid for decision boundary
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                     np.linspace(y_min, y_max, 300))

Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# ⿦ Plot decision boundaries
plt.figure(figsize=(10, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.Set2)
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train,
            edgecolor='k', s=70, label="Train", cmap=plt.cm.Set2)
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test,
            marker='*', s=150, edgecolor='k', label="Test", cmap=plt.cm.Set2)

plt.title("Naive Bayes Decision Boundaries (Iris Dataset)")
plt.xlabel("Sepal length")
plt.ylabel("Sepal width")
plt.legend()
plt.show()