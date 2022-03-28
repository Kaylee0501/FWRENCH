import numpy as np
from sklearn.decomposition import PCA
#from PIL import Image
#import sys
# from os import walk
# from os import path
# import json
from wrench.dataset import load_dataset

'''
see basketball.py in running_examples, use load_dataset so that
1. it receives train, test, eval classes,
2. unpackage them to np arrays (see snuba_lf_selector.py for how)
3. do pca things,
4. repackage them back to train, test, eval classes
'''

def to_embedding(features, n_components):
    pca = PCA(n_components=n_components)
    embedding = pca.fit_transform(features)
    return embedding

def packup(data_split, fitted_transform):
    i = 0
    for d in data_split.examples:
        d['feature'] = fitted_transform[i]

    return data_split

def fit(dataset, num_c=3):
    #dataset = sys.argv[1]
    dataset = dataset
    #num_comp = int(sys.argv[2])
    num_comp = num_c

    dataset_home = '../../datasets'
    data = dataset
    train_data, valid_data, test_data = load_dataset(
        dataset_home, data, 
        extract_feature=False, 
        extract_fn=None)

    #print(type(valid_data))

    x_train = np.array([d['feature'] for d in train_data.examples])
    x_valid = np.array([d['feature'] for d in valid_data.examples])
    x_test = np.array([d['feature'] for d in test_data.examples])
    train_transform = to_embedding(x_train, num_comp)
    valid_transform = to_embedding(x_valid, num_comp)
    test_transform = to_embedding(x_test, num_comp)
    #print("line 51")
    #print(test_transform)
    train_data = packup(train_data, train_transform)
    valid_data = packup(valid_data, valid_transform)
    test_data = packup(test_data, test_transform)
    
    return train_data, valid_data, test_data
