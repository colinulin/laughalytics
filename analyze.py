#!/usr/bin/python

# sudo time python analyze.py notlaughs_3.wav

from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from features import mfcc
from features import logfbank
from bunch import *
import sys
import os
import bunch
import numpy
import csv
import time
import scipy.io.wavfile as wav

numpy.set_printoptions(threshold=numpy.nan)

# Get arguments
audiofile = sys.argv[1]

# Get time signature
timesigtest = (audiofile.split('-').pop()).split('.')[0]
try: 
    int(timesigtest)
    timesig = timesigtest
except ValueError:
    timesig = str(int(time.time()))

# Load music file
(rate,sig) = wav.read(audiofile)
mfcc_feat = mfcc(sig,samplerate=rate,lowfreq=100,highfreq=10000)

# Put data into array
data = mfcc_feat

# Apply Scaler
scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
data = scaler.fit_transform(data)

# Delete 1st value
data = numpy.delete(data,0,1)

# Get Delta
data = numpy.diff(data, axis=0)

# Group
groups = []
for i in range(0, numpy.size(data,0)):
	groups.append(data[i:i+72,].flatten())

# Remove shorter arrays (eventually this will grab the beginning of the next audio) so they're all the same length
gooddata = []
maxlen = len(groups[0])
for group in groups:
	if len(group) == maxlen:
		gooddata.append(group)

# Load the knowledge file
clf = joblib.load('brain/knowledge.pkl')

# Get results
results = clf.predict_proba(gooddata)

count = 0
for test in numpy.around(results, 2):
	if test[1] > .66:
		count += 1

with open("results.csv", "a") as results_file:
    results_file.write(str(count / len(results)) + ',' + timesig + ',' + audiofile + '\n')
results_file.close()

# os.remove(audiofile)

