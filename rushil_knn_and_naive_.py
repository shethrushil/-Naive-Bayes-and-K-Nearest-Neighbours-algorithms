# -*- coding: utf-8 -*-
"""Rushil KNN and Naive .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f0AKFpw_ktYrJQB9R0_Enr_h1AfFLbC-

rushilsheth7171@gmail.com
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Read the CSV files
df = pd.read_csv(r"C:\Users\rushil\Downloads\titanic\train.csv")
df_test = pd.read_csv(r"C:\Users\rushil\Downloads\titanic\test.csv")

# Drop unnecessary columns
df.drop(["Cabin", "Name", "PassengerId", "Ticket"], axis=1, inplace=True)
df_test.drop(["Cabin", "Name", "PassengerId", "Ticket"], axis=1, inplace=True)

# Map categorical variables to numerical values
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df['Embarked'] = df['Embarked'].map({'S': 1, 'C': 2, 'Q': 3})

# Handle missing values and bin numerical variables
df['Age'] = df['Age'].fillna(method='backfill')
df['Embarked'] = df['Embarked'].fillna(method='ffill')

df = df[['Age', 'Embarked', 'Fare', 'Parch', 'Pclass', 'Sex', 'SibSp', 'Survived']]
df_test = df_test[['Age', 'Embarked', 'Fare', 'Parch', 'Pclass', 'Sex', 'SibSp']]

# Bin the 'Age' variable
data = [df, df_test]
for d in data:
    d['Age'] = d['Age'].fillna(-1).astype(int)
    d.loc[d['Age'] <= 10, 'Age'] = 0
    d.loc[(d['Age'] > 10) & (d['Age'] <= 18), 'Age'] = 1
    d.loc[(d['Age'] > 18) & (d['Age'] <= 25), 'Age'] = 2
    d.loc[(d['Age'] > 25) & (d['Age'] <= 30), 'Age'] = 3
    d.loc[(d['Age'] > 30) & (d['Age'] <= 35), 'Age'] = 4
    d.loc[(d['Age'] > 35) & (d['Age'] <= 40), 'Age'] = 5
    d.loc[(d['Age'] > 40) & (d['Age'] <= 65), 'Age'] = 6
    d.loc[d['Age'] > 65, 'Age'] = 6

# Bin the 'Fare' variable
data = [df, df_test]
for d in data:
    d.loc[d['Fare'] <= 8, 'Fare'] = 0
    d.loc[(d['Fare'] > 8) & (d['Fare'] <= 15), 'Fare'] = 1
    d.loc[(d['Fare'] > 15) & (d['Fare'] <= 31), 'Fare'] = 2
    d.loc[(d['Fare'] > 31) & (d['Fare'] <= 99), 'Fare'] = 3
    d.loc[(d['Fare'] > 99) & (d['Fare'] <= 250), 'Fare'] = 4
    d.loc[d['Fare'] > 250, 'Fare'] = 5
    d['Fare'] = d['Fare'].fillna(-1).astype(int)

# Convert 'Survived' column to integer type
df.Survived = df.Survived.astype(int)

# Split the data into training and test sets
train, test = train_test_split(df, test_size=0.2)

# Calculate prior probabilities of survival and non-survival
survived_yes = train.loc[train.Survived == 1]
P_yes = len(survived_yes) / len(train)

survived_no = train.loc[train.Survived == 0]
P_no = len(survived_no) / len(train)

# Create a DataFrame to store actual and predicted values
output_dataframe = pd.DataFrame(columns=['Actual', 'Predicted'])

# Iterate over each row in the test set
# Iterate over each row in the test set
for row in test.itertuples(index=False):
    test1 = list(row[:-1])  # Exclude the last element (actual value)
    ans = row[-1]  # Last element is the actual value

    py = 1
    for j in range(len(test1)):
        val = train[(train[train.columns[j]] == test1[j]) & (train.Survived == 1)].shape[0]
        py *= val / len(survived_yes)
    total_yes = py * P_yes

    pn = 1
    for j in range(len(test1)):
        val = train[(train[train.columns[j]] == test1[j]) & (train.Survived == 0)].shape[0]
        pn *= val / len(survived_no)
    total_no = pn * P_no

    # Compare probabilities and assign predicted value
    if total_yes > total_no:
        list1 = [[ans, 1]]
        output_dataframe = output_dataframe.append(pd.DataFrame(list1, columns=['Actual', 'Predicted']), ignore_index=True)
    else:
        list0 = [[ans, 0]]
        output_dataframe = output_dataframe.append(pd.DataFrame(list0, columns=['Actual', 'Predicted']), ignore_index=True)

# Calculate true positives, true negatives, false positives, and false negatives
TP = output_dataframe[(output_dataframe['Predicted'] == 1) & (output_dataframe['Actual'] == 1)].shape[0]
TN = output_dataframe[(output_dataframe['Predicted'] == 0) & (output_dataframe['Actual'] == 0)].shape[0]
FP = output_dataframe[(output_dataframe['Predicted'] == 1) & (output_dataframe['Actual'] == 0)].shape[0]
FN = output_dataframe[(output_dataframe['Predicted'] == 0) & (output_dataframe['Actual'] == 1)].shape[0]

# Calculate accuracy, precision, and recall
accuracy = (TP + TN) / len(output_dataframe)
print("The accuracy for the test set is", accuracy * 100, "%")

precision = TP / (TP + FP)
print("The precision for the test set is", precision * 100, "%")

recall = TP / (TP + FN)
print("The recall for the test set is", recall * 100, "%")

#knn

# Split the data into training and test sets
train, test = train_test_split(df, test_size=0.2)

# Calculate prior probabilities of survival and non-survival
survived_yes = train.loc[train.Survived == 1]
P_yes = len(survived_yes) / len(train)

survived_no = train.loc[train.Survived == 0]
P_no = len(survived_no) / len(train)

# Create a DataFrame to store actual and predicted values
output_dataframe = pd.DataFrame(columns=['Actual', 'Predicted'])

# Iterate over each row in the test set
for row in test.itertuples(index=False):
    test1 = list(row[:-1])  # Exclude the last element (actual value)
    ans = row[-1]  # Last element is the actual value

    distances = []
    for train_row in train.itertuples(index=False):
        train1 = list(train_row[:-1])
        distance = np.sqrt(np.sum(np.square(np.subtract(train1, test1))))
        distances.append((train1, distance))

    # Sort distances in ascending order
    distances.sort(key=lambda x: x[1])

    k = 5  # Set the value of K (number of neighbors)
    neighbors = [item[0] for item in distances[:k]]

    total_yes = sum(1 for neighbor in neighbors if neighbor[-1] == 1)
    total_no = sum(1 for neighbor in neighbors if neighbor[-1] == 0)

    # Compare counts and assign predicted value
    if total_yes > total_no:
        list1 = [[ans, 1]]
        output_dataframe = output_dataframe.append(pd.DataFrame(list1, columns=['Actual', 'Predicted']), ignore_index=True)
    else:
        list0 = [[ans, 0]]
        output_dataframe = output_dataframe.append(pd.DataFrame(list0, columns=['Actual', 'Predicted']), ignore_index=True)

# Calculate true positives, true negatives, false positives, and false negatives
TP = output_dataframe[(output_dataframe['Predicted'] == 1) & (output_dataframe['Actual'] == 1)].shape[0]
TN = output_dataframe[(output_dataframe['Predicted'] == 0) & (output_dataframe['Actual'] == 0)].shape[0]
FP = output_dataframe[(output_dataframe['Predicted'] == 1) & (output_dataframe['Actual'] == 0)].shape[0]
FN = output_dataframe[(output_dataframe['Predicted'] == 0) & (output_dataframe['Actual'] == 1)].shape[0]

# Calculate accuracy, precision, and recall
accuracy = (TP + TN) / len(output_dataframe)
print("The accuracy for the test set is", accuracy * 100, "%")

precision = TP / (TP + FP)
print("The precision for the test set is", precision * 100, "%")

recall = TP / (TP + FN)
print("The recall for the test set is", recall * 100, "%")