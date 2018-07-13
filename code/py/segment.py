# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:12:31 2017

@author: Mark
"""


import ellipse_tool as et
import math
import numpy as np
import feature
import enums


class Segment:

    #Constructor methods =======================================================================================

    def __init__(self, traj, lseg, ovlp, cum_dist_end_prev, arena):
        
        #output - features
        self.features = None
        
        #input
        self.segment_data, self.last_value_segment, self.end_of_trajectory = self.getSegment(traj, lseg, ovlp, cum_dist_end_prev)
        self.segment_length = self.getSegmentLength(self.segment_data)
        self.arena = arena
        
        #segment info
        self.points = None
        self.ellipse = None
        self.min_enclosing_ellipse_area = None
        self.min_enclosing_ellipse_area = None
        self.ellipse_a_axis = None
        self.ellipse_b_axis = None
        first_row_segment = self.segment_data.iloc[0]
        self.segmentID = str(first_row_segment['filename']) + \
                         "--" + \
                         first_row_segment['ExperimentName'] + \
                         int(first_row_segment['UsingLight']) * "UsingLight" + \
                         int(not first_row_segment['UsingLight']) * "WithoutLight" + \
                         str(first_row_segment['frames.comb'])
        self.filename = first_row_segment['filename']
        self.experiment_name = first_row_segment['ExperimentName']
        self.using_light = first_row_segment['UsingLight']
        
        #calculations
        if self.segment_data.shape[0]>2:
            self.calcFeatures()    
        
    #helper methods =======================================================================================
                
    def findMinEnclosingEllipse(self, points):
        ellipse = et.EllipseTool()
        ellipse.calcMinAreaEllipse(points)
        return(ellipse)
        
    def calcMinEnclosingEllipseArea(self, radii):
        return(radii[0] * radii[1]*math.pi)
        
    def calcAxisMinEnclosingEllipse(self, radii):
        return(max(radii), min(radii))
        
    def extractPointsFromDataTable(self):
        #print(np.array([self.segment_data["x_mm"],self.segment_data["y_mm"]]).T)
        return(np.array([self.segment_data["x_mm"],self.segment_data["y_mm"]]).T) 
        
    def getFeature(self, eFeature):
        return(self.features[eFeature])
        
    def getSegment(self, traj, lseg, ovlp, cum_dist_end_prev):
        
        cumdist = traj['CumulativeDistance']
        
        #find the beginning of this segment
        if cum_dist_end_prev != 0:

#            distance_to_previous_point = traj['Distance'][traj['CumulativeDistance'] == cum_dist_end_prev].iloc[0]
#            if distance_to_previous_point >= lseg:
#                value_just_below = cum_dist_end_prev    
#            else:
            max_cum_dist_start_second = cum_dist_end_prev - lseg*ovlp
            values_greater = cumdist[cumdist > max_cum_dist_start_second]
            value_just_below = values_greater.iloc[0]
                
            start_seg_index = cumdist[cumdist==value_just_below].index[0]
            
        else:
            value_just_below = 0
            start_seg_index = 0
            
        #find the end of this segment
        values_greater = traj['CumulativeDistance'][traj['CumulativeDistance'] >= value_just_below + lseg]
        if values_greater.size == 0:
            last_value_segment = None
            segment = traj.loc[start_seg_index:,:].reset_index(drop=True)
            end_of_trajectory = True
        else:
            last_value_segment = values_greater.iloc[0]
            cumdist = traj['CumulativeDistance']
            end_seg_index = cumdist[cumdist==last_value_segment].index[0]
            segment = traj.loc[start_seg_index:end_seg_index,:]
            segment = segment.reset_index(drop=True)
            end_of_trajectory = False
        
        return segment, last_value_segment, end_of_trajectory
        
    def getSegmentLength(self, segment):
        
        start = segment["CumulativeDistance"].iloc[0]
        end = segment["CumulativeDistance"].iloc[-1]
        
        return(end - start)
        
    #main routine that is called when segment is constructed==============================================
        
    def calcFeatures(self):         
        
        self.points = self.extractPointsFromDataTable()
        self.ellipse = self.findMinEnclosingEllipse(self.points)
        self.min_enclosing_ellipse_area = self.calcMinEnclosingEllipseArea(self.ellipse.radii)
        self.ellipse_a_axis, self.ellipse_b_axis = self.calcAxisMinEnclosingEllipse(self.ellipse.radii)
        
        self.features = [feature.MedianDistanceFromCentre(self, enums.eFeature.MedianDistanceFromCentre),
                         feature.IQRange(self, enums.eFeature.IQRange),
                         feature.Focus(self, enums.eFeature.Focus),
                         feature.Eccentricity(self, enums.eFeature.Eccentricity),
                         #feature.MaximumLoop(self, enums.eFeature.MaximumLoop),
                         feature.InnerRadiusVariation(self, enums.eFeature.InnerRadiusVariation),
                         feature.CentralDisplacement(self, enums.eFeature.CentralDisplacement),
#                         feature.MeanSpeed(self, enums.eFeature.MeanSpeed),
#                         feature.MinSpeed(self, enums.eFeature.MinSpeed),
#                         feature.MaxSpeed(self, enums.eFeature.MaxSpeed),
#                         feature.MedianSpeed(self, enums.eFeature.MedianSpeed),
#                         feature.IQSpeed(self, enums.eFeature.IQSpeed),
#                         feature.MeanRotation(self, enums.eFeature.MeanRotation),
#                         feature.MedianRotation(self, enums.eFeature.MedianRotation),
#                         feature.MinRotation(self, enums.eFeature.MinRotation),
#                         feature.MaxRotation(self, enums.eFeature.MaxRotation),
#                         feature.IQRotation(self, enums.eFeature.IQRotation),
#                         feature.MeanAbsRotation(self, enums.eFeature.MeanAbsRotation),
#                         feature.MedianAbsRotation(self, enums.eFeature.MedianAbsRotation),
#                         feature.MinAbsRotation(self, enums.eFeature.MinAbsRotation),
#                         feature.MaxAbsRotation(self, enums.eFeature.MaxAbsRotation),
#                         feature.IQAbsRotation(self, enums.eFeature.IQAbsRotation),
                         feature.PathEfficiency(self, enums.eFeature.PathEfficiency),
                         feature.SumAbsoluteAngles(self, enums.eFeature.SumAbsoluteAngles)
                         #feature.LocationDensity(self, enums.eFeature.LocationDensity)
                         ]

