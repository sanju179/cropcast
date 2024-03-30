import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('static/fertilizer.csv')
features = df[['Nitrogen', 'Potassium','Phosphorous']]
target = df['Fertilizer Name']
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.3,random_state =0)

RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain,Ytrain)

predicted_values = RF.predict(Xtest)

N=104
P=18
K=30


def predict_fertilizer(N,P,K):
    fertiliser_recommend = []
    data = np.array([[N,P,K]])
    probabilities =RF.predict_proba(data)  # Selecting probabilities for the first sample in X_test
    classes=RF.classes_

    dictionary = dict(zip(classes, probabilities[0]))
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    fcount=0
    for i in sorted_dict.keys():
        if fcount<2:
            fertiliser_recommend.append(i)
            fcount+=1
    
    return fertiliser_recommend