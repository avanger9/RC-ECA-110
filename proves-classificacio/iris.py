#!../python3.9/bin/python

import numpy as np
from sklearn.datasets import load_iris
from sklearn.svm import SVC as svc

data = load_iris()

tn = data.target_names
fn = data.feature_names
print(fn, tn)

d = data.data
t = data.target

print('shape of data:', d.shape, 'shape of target:', t.shape)
print(d[:5], '\n', t[:5])

clf = svc()
clf.set_params(kernel='linear')
clf.fit(d,t)
print(clf.predict(data.data[:3]))

clf.fit(d,tn[t])
print(clf.predict(data.data[45:55]))

# import pdb; pdb.set_trace()
