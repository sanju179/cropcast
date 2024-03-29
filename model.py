import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

df = pd.read_csv('static/Crop_recommendation.csv')

features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.3,random_state =0)

SVM = SVC(kernel="poly") # use of linear- 0.989 accuracy
SVM.probability=True
SVM.fit(Xtrain,Ytrain)
predicted_values = SVM.predict(Xtest)
x = metrics.accuracy_score(Ytest, predicted_values)
print("SVM's Accuracy is: ", x)

'''N = 104
P = 18
K = 30
temperature = 43.603016
humidity = 69.3
ph = 6.7
rainfall = 110.91'''

def predict_crop(N,P,K,temperature,humidity,ph,rainfall):

    data = np.array([[N,P, K, temperature, humidity,ph, rainfall]])
    probabilities =SVM.predict_proba(data)  # Selecting probabilities for the first sample in X_test
    classes=SVM.classes_

    dictionary = dict(zip(classes, probabilities[0]))
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    top3_recommendations=[]
    top=0
    for i in sorted_dict.keys():
        if top<3:
            top3_recommendations.append(i)
            top+=1
    return  top3_recommendations

#print(predict_crop(104,18,30,43.6,69.3,6.7,110.9))

