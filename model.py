'''
Created on Feb 24, 2018

'''
import time
import pickle
from sklearn.svm import LinearSVC
from corpus import build_features
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer  
    
dev_path = 'conll-2012/dev/english/annotations'
train_path = 'conll-2012/train/english/annotations'
test_path = 'conll-2012/test/english/annotations'

start = time.time()    

print("Parsing files and extracting features...")
X_train, y_train = build_features(train_path)

print("Training model...")
vec = DictVectorizer()
X_train = vec.fit_transform(X_train)
   
#build model
#clf = LogisticRegression()
#model = clf.fit(X_train, y_train)

clf = LinearSVC() 
model = clf.fit(X_train, y_train)

#Validate the model
X_dev, y_dev = build_features(dev_path)

print("Testing model...")
X_dev = vec.transform(X_dev)
pred = model.predict(X_dev)
  
print("F1: ", f1_score(y_dev, pred, average='macro'))

end = time.time()
pickle.dump(model, open("svm.model", 'wb'))
print("Saving to model...")
print("Total time used: ", (end - start)/3600)