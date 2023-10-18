import h5py
import argparse
import numpy as np
import json

parser = argparse.ArgumentParser()
parser.add_argument('feature_file', type=str)
parser.add_argument('start', type=int, default=0)
parser.add_argument('end', type=int, default=10)
parser.add_argument('--top', type=int, default=6)
parser.add_argument('--dataset_name', type=str, default='features')

args = parser.parse_args()
start = args.start
end = args.end

feature_set = set()
coll = []
with h5py.File(args.feature_file,'r') as f:
    data = f[args.dataset_name][start:end]
    for i in range(len(data)): 
        # Read row i from np array
        feature_vector = data[i,:]
        # Sort the feature vector, then read from its tail and select the top features since argsort does ascending sort
        topFeatureIds = np.argsort(feature_vector)[::-1][:args.top]
        coll.append(list(topFeatureIds))
        for ff in topFeatureIds:
            feature_set.add(int(ff))

fname = 'distinct_features_t' + str(args.top) + '.json'
with open(fname,'w') as f:
        json.dump(list(feature_set), f)

fname = 'top' + str(args.top) + '.json'
with open(fname,'w') as f:
        json.dump(coll,f)

