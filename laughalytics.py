#!/usr/bin/python

# Expects a laughs.wav file and a notlaughs.wav file in the same folder
# Also expects a folder called "brain" in same folder to store the knowledge.pkl file
# sudo python laughalytics.py

from sklearn import datasets
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from features import mfcc
from features import logfbank
from bunch import *
import sys
import bunch
import numpy
import scipy
import scipy.io.wavfile as wav
import os.path

# Get arguments
laughfile = 'audio/recording-breakfast-iphone-laughs-first.wav' # update to your laugh file
notlaughfile = 'audio/recording-breakfast-iphone-not-laughs-first.wav' # update to your file that doesn't have laughs

# Load music file
(laughrate,laughsig) = wav.read(laughfile)
laugh_mfcc_feat = mfcc(laughsig,samplerate=laughrate,lowfreq=100,highfreq=10000)
(notrate,notsig) = wav.read(notlaughfile)
not_mfcc_feat = mfcc(notsig,samplerate=notrate,lowfreq=100,highfreq=10000)

# Put data into array
laugh_data = laugh_mfcc_feat
not_data = not_mfcc_feat

# Apply Scaler
scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
laugh_data = scaler.fit_transform(laugh_data)
not_data = scaler.fit_transform(not_data)

# Delete 1st value
laugh_data = numpy.delete(laugh_data,0,1)
not_data = numpy.delete(not_data,0,1)

# Get Delta
laugh_data = numpy.diff(laugh_data, axis=0)
not_data = numpy.diff(not_data, axis=0)

# Mark each line as laugh or not
target = []
for line in laugh_data:
	target.append(1)
for line in not_data:
	target.append(0)

# Group
laugh_groups = []
for i in range(0, numpy.size(laugh_data,0)):
	laugh_groups.append(laugh_data[i:i+72,].flatten())

not_groups = []
for i in range(0, numpy.size(not_data,0)):
	laugh_groups.append(not_data[i:i+72,].flatten())

# Group laughs and not laughs
groups = numpy.concatenate((laugh_groups, not_groups), axis=0)

# Remove shorter arrays (eventually this will grab the beginning of the next audio) so they're all the same length
gooddata = []
goodtarget = []
maxlen = len(groups[0])
for i in range(0, numpy.size(groups,0)):
	if len(groups[i]) == maxlen:
		gooddata.append(groups[i])
		goodtarget.append(target[i])

# Configure test settings
# Train using Multi-Layer Perceptron
# http://scikit-learn.org/dev/modules/neural_networks_supervised.html
if os.path.isfile('brain/knowledge.pkl'):
	clf = joblib.load('brain/knowledge.pkl')
else:
	clf = MLPClassifier(algorithm='adam', alpha=1e-5, hidden_layer_sizes=(200,), random_state=1, max_iter=1000000000, warm_start = True, tol=0.00000001)

# Learn
clf.fit(gooddata, goodtarget)

# Store new knowledge
# http://scikit-learn.org/stable/modules/model_persistence.html#model-persistence
joblib.dump(clf, 'brain/knowledge.pkl')



