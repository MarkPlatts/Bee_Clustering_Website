# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 17:51:44 2017

@author: Mark
"""

from sklearn import preprocessing
from sklearn.cluster import KMeans

#functions start ====================================================================

def perform_kmeans(df, n_clusters):
    
    clusterer = KMeans(n_clusters = n_clusters, random_state = 0, max_iter = 1000)
    k_means = clusterer.fit(df.iloc[:,:])
    
    return(k_means.labels_, k_means.cluster_centers_)
    
def scale_features(x):
    std_scaler = preprocessing.StandardScaler()
    x_scaled = std_scaler.fit_transform(x)
    return(x_scaled)

#functions end ====================================================================


