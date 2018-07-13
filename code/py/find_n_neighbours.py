# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:29:38 2017

@author: Mark
"""

import numpy as np

def findNNearestNeighbours(df, n_nearest, kmean):
    """Finds the segmentID's for n nearest neighbours of a given kmeans center
    
    Parameters
    ----------
    df : pandas.dataframe
        A data frame where each row contains the features for a given segment
    n_nearest : integer
        The number of nearest neighbours to find.  
    kmean : dict
        A dictionary containing the feature names and values for a given kmeans
        centre.  
        
    Returns
    -------
    pandas.core.series.Series
        A series contain the segmentID's for the n closest neighbours to the
        given kmeans centre.
    
    """
    
    n_obs = df.shape[0]
    list_of_sse = []
    
    for iobs in range(0, n_obs):
        sse = 0.0    
        for feature_name, feature_value in kmean.items():
            #print(feature_name, feature_value)
            df_value = df.iloc[iobs][feature_name]
            kmean_value = feature_value
            sse = sse + (df_value - kmean_value)**2
        list_of_sse.append(sse)
        

    df_sort = df
    df_sort['sse'] = np.asarray(list_of_sse)
    df_sort = df_sort.sort_values('sse')   

    df_top_n_value = df_sort.iloc[0:n_nearest,:]
    
    return(df_top_n_value['SegmentID'])
    
# end functions ====================================================================