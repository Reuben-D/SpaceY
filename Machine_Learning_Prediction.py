# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:54:02 2024

@author: Reuben Dlamini
"""

#import piplite
#await piplite.install(['numpy'])
#await piplite.install(['pandas'])
#await piplite.install(['seaborn'])

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
# Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standardize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
#from sklearn.neighbors import KNeighborsClassifier

# Function to plot confusion matrix
def plot_confusion_matrix(y, y_predict):
    "This function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax)  # annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(['did not land', 'landed'])
    ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

import requests
import io

# URLs to the CSV files
URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
URL2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv"

# Function to fetch CSV data from a URL and return it as a DataFrame
def fetch_csv_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Read the content into a DataFrame
        data = pd.read_csv(io.StringIO(response.text))
        return data
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

# Fetch data from the two URLs
data = fetch_csv_data(URL1)
X = fetch_csv_data(URL2)

# Display the first few rows of each DataFrame
if data is not None:
    print("Data from URL1 (dataset_part_2.csv):")
    print(data.head())

if X is not None:
    print("Data from URL2 (dataset_part_3.csv):")
    print(X.head())




'''from js import fetch
import io

URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
resp1 = await fetch(URL1)
text1 = io.BytesIO((await resp1.arrayBuffer()).to_py())
data = pd.read_csv(text1)

URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
resp2 = await fetch(URL2)
text2 = io.BytesIO((await resp2.arrayBuffer()).to_py())
X = pd.read_csv(text2)'''

# Step 1: Create a NumPy array from the column Class in data
Y = data['Class'].to_numpy()
print(Y[:10])

# Step 2: Standardize the data in X
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)

# Step 3: Split the data into training and test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Step 4: Create a logistic regression object and a GridSearchCV object for Logistic Regression
parameters = {"C": [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters, cv=10)
logreg_cv.fit(X_train, Y_train)

# Output the best parameters and accuracy for Logistic Regression
print("tuned hyperparameters: (best parameters) ", logreg_cv.best_params_)
print("accuracy: ", logreg_cv.best_score_)

# Step 5: Calculate accuracy on the test data using Logistic Regression
Bestlogreg_cv = logreg_cv.best_estimator_
logistic_reg = Bestlogreg_cv.score(X_test, Y_test)
print(logistic_reg)

# Plot confusion matrix for Logistic Regression
yhat = logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# Step 6: Create a support vector machine object and a GridSearchCV object for SVM
parameters = {'kernel': ('linear', 'rbf', 'poly', 'sigmoid'), 'C': np.logspace(-3, 3, 5), 'gamma': np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters, cv=10)
svm_cv.fit(X_train, Y_train)

# Output the best parameters and accuracy for SVM
print("tuned hyperparameters: (best parameters) ", svm_cv.best_params_)
print("accuracy: ", svm_cv.best_score_)

# Step 7: Calculate accuracy on the test data using SVM
bestsvm_cv = svm_cv.best_estimator_
svm_score = bestsvm_cv.score(X_test, Y_test)
print(svm_score)

# Plot confusion matrix for SVM
yhat = svm_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# Step 8: Create a decision tree classifier object and a GridSearchCV object for Decision Trees
parameters = {'criterion': ['gini', 'entropy'], 'splitter': ['best', 'random'], 'max_depth': [2 * n for n in range(1, 10)], 'max_features': ['sqrt'], 'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters, cv=10)
tree_cv.fit(X_train, Y_train)

# Output the best parameters and accuracy for Decision Tree
print("tuned hyperparameters: (best parameters) ", tree_cv.best_params_)
print("accuracy: ", tree_cv.best_score_)

