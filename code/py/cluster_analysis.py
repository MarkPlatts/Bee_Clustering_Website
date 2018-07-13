# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 08:33:59 2017

@author: Mark
"""

#initialisation start ====================================================================

import perform_kmeans as pkm
import os
import pandas as pd
import plot_segment
import find_n_neighbours as n_neigh


def plot_n_nearest(seg_length, n_clusters, n_nearest_neighbours):
    """Plots the n nearest neighbours to each of the cluster centres
    
    Parameters
    ----------
    seg_length : float
        The length of segment being considered.
    n_clusters : int
        The number of centres used by the kmeans algorithm.
    n_nearest_neighbours: int
        The number of segments to plot nearest to each kmean centre.
    """
    
    #load data
    path = os.path.join("../../Data/length" + str(seg_length))
    df_features = pd.read_csv(os.path.join(path, "segment_features.csv"))
    df_xy = pd.read_csv(os.path.join(path, "segment_xys.csv"))
    df_for_arena_dims = plot_segment.load_df_for_arena_dims()
    
    #scale the features
    df_features.iloc[:,4:12] = pkm.scale_features(df_features.iloc[:,4:12])
    
    #perform kmeans
    cluster_labels, cluster_centres = pkm.perform_kmeans(df = df_features.iloc[:,4:12], n_clusters = n_clusters)
    
    #init plotting
    plot_index = 0 #this is used to specify position in matrix of plots
    
    for cluster_id in range(0, n_clusters):
        
        #retrieve the cluster centre
        kmean_feature_vals = {'MedianDistanceFromCentre': cluster_centres[cluster_id, 0], 
                              'IQRange': cluster_centres[cluster_id, 1],
                              'Focus': cluster_centres[cluster_id, 2],
                              'Eccentricity': cluster_centres[cluster_id, 3],
                              'InnerRadiusVariation': cluster_centres[cluster_id, 4],
                              'CentralDisplacement': cluster_centres[cluster_id, 5],
                              'PathEfficiency': cluster_centres[cluster_id, 6],
                              'SumAbsoluteAngles': cluster_centres[cluster_id, 7]}
        
        #get the segmentIDs for n nearest neighbours to cluster centres
        segmentIDs = n_neigh.findNNearestNeighbours(df_features, n_nearest_neighbours, kmean_feature_vals)
        
        #plot the segments
        for iseg in segmentIDs:
            df_xy_temp = df_xy[df_xy['SegmentID'] == iseg]
            plot_index = plot_index + 1
            plot_title = "ClusterID: " + str(cluster_id)
            plot_segment.plot_all(df_plot_arena = df_for_arena_dims,
                                  seg = df_xy_temp,
                                  index = plot_index,
                                  n_rows = n_clusters,
                                  n_cols = n_nearest_neighbours,
                                  title = plot_title)
                                  