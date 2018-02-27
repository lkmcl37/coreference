'''
Created on Feb 24, 2018

'''
from sklearn.svm import SVC 
from corpus import build_features
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer  
    
dev_path = 'conll-2012/dev/english/annotations'
train_path = 'conll-2012/train/english/annotations'
test_path = 'conll-2012/test/english/annotations'
    
#Vectorize the features and train the model
vec = DictVectorizer()

print("Parsing files and extracting features...")
X_train, y_train = build_features(train_path)

print("Training model...")
X_train = vec.fit_transform(X_train)
   
#build model
#clf = LogisticRegression()
#model = clf.fit(X_train, y_train)

clf = SVC()  
clf.fit(X_train, y_train)

#Validate the model
X_dev, y_dev = build_features(dev_path)

print("Testing model...")
X_dev = vec.transform(X_dev)
#pred = model.predict(X_dev)
pred = clf.predict(X_dev)
  
print(f1_score(y_dev, pred, average='macro'))