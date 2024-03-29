import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,accuracy_score


dt = pd.read_csv(r'static\fertilizer.csv')
dt.head()

X = dt.drop(columns=['Fertilizer Name'])
y = dt['Fertilizer Name']

X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.7,shuffle=True,random_state=42)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
encode_ferti = LabelEncoder()
dt['Fertilizer Name']=encode_ferti.fit_transform(dt['Fertilizer Name'])

y_train_encoded = encode_ferti.fit_transform(y_train)
y_test_encoded = encode_ferti.transform(y_test)
# random forest
classifier = RandomForestClassifier(n_estimators=100, random_state=124)
classifier.fit(X_train, y_train_encoded)

# svm
svmc = SVC(kernel='sigmoid',random_state=42)
svmc.fit(X_train, y_train_encoded)

y_pred = classifier.predict(X_test)

y_svmpred = svmc.predict(X_test)

cm = confusion_matrix(y_test_encoded,y_pred)
accuracy_score(y_test_encoded,y_pred)

cmsvm = confusion_matrix(y_test_encoded,y_pred)
print("SVM's Accuracy for fertilizer is: ", accuracy_score(y_test_encoded,y_svmpred))

""" 
feat = np.array([[18,46,0]])
res = classifier.predict(feat)[0]

rest = svmc.predict(feat)[0] """

def predict_fertilizer(n, p, k):
    np_array = np.array([[n, p, k]])
    scaled_np_array = sc.transform(np_array)

    predicted_fertilizer = svmc.predict(scaled_np_array)[0]

    decoded_fertilizer = encode_ferti.inverse_transform([predicted_fertilizer])[0]
    
    return decoded_fertilizer

n_value = 90
p_value = 16
k_value = 50
predicted_fertilizer = predict_fertilizer(n_value, p_value, k_value)
print("Predicted Fertilizer:", predicted_fertilizer)


