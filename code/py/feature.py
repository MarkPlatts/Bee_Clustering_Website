# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 07:59:01 2017

@author: Mark
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 04:12:44 2017

@author: Mark
"""

from abc import ABCMeta, abstractmethod
import numpy as np
import math
import loop_tool as lt
from scipy.special import comb
import logging
#import enumFeature.enumFeature

class Feature:
    """Abstract feature class
    
    Parameters
    ----------
    segment : Segment
        The segment for which the given feature is being calculated.
    enumFeature : enums.eFeature
        Gave an index number relating to the feature name. This was poor
        constructed and I don't think it works anymore. It identifying the
        position of a value in a list, but since certain features were
        deleted, the index no longer pointed to the correct position. Should
        have probably used a dictionary data type.        
        
    Attributes
    ----------
    print_feature_names : boolean
        Set to True if you want the feature name to be printed to the log file.
    segment : Segment
        The segment for which the given feature is being calculated.
    value : float
        The feature value calculated.  
    name : string
        The name of the feature.  
    enumFeature : enums.eFeature
        See Parameters above.  
        
    """    
    
    __metaclass__ = ABCMeta
    
    index = -1
    
    def __init__(self, segment, enumFeature):
        self.print_feature_names = True
        self.segment = segment
        self.value = self.calculateFeature()
        self.name = self.featureName()
        self.enumFeature = enumFeature
    
    @abstractmethod
    def featureName(self):
        pass
    
    @abstractmethod
    def calculateFeature(self):
        pass

        
class MedianDistanceFromCentre(Feature):
    
    def featureName(self):
        return "MedianDistanceFromCentre"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        median = self.segment.segment_data["DistanceCentre"].median()/(self.segment.arena.diameter/2.0)
        return(median)   
        
class IQRange(Feature):
    
    def featureName(self):
        return "IQRange"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        LQ = self.segment.segment_data["DistanceCentre"].quantile(0.25)
        UQ = self.segment.segment_data["DistanceCentre"].quantile(0.75)
        IQRange = (UQ - LQ)/(self.segment.arena.diameter/2.0)
        return(IQRange)
        
class Focus(Feature):
    
    def featureName(self):
        return "Focus"
    
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        return(1 - 4 * self.segment.min_enclosing_ellipse_area/(math.pi*self.segment.segment_length**2))

class Eccentricity(Feature):
    
    def featureName(self):
        return "Eccentricity"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        return(math.sqrt(1 - (self.segment.ellipse_b_axis**2)/(self.segment.ellipse_a_axis**2)))
        
class MaximumLoop(Feature):
    
    def featureName(self):
        return "MaximumLoop"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())    
        max_length = 0
        
        segment_data = self.segment.segment_data.drop_duplicates(subset=['x_mm', 'y_mm'])
        
        #find out how many points their are
        nPoints = segment_data.shape[0] #This is the number of lines to check for intersection
        #print("nPoints:", nPoints)
        for iLines1 in range(0,nPoints-3):
            #create line between current point and next point
            line1 = {'x1': segment_data['x_mm'].iloc[iLines1], 
                     'y1': segment_data['y_mm'].iloc[iLines1],
                     'x2': segment_data['x_mm'].iloc[iLines1+1],
                     'y2': segment_data['y_mm'].iloc[iLines1+1]}
            for iLines2 in range(iLines1+2, nPoints-1): 
                #loop over subsequent lines check if there is a line that intersects and calculating
                #the length between them
                #print("iLines2+1:", iLines2+1)
                line2 = {'x1': segment_data['x_mm'].iloc[iLines2], 
                         'y1': segment_data['y_mm'].iloc[iLines2],
                         'x2': segment_data['x_mm'].iloc[iLines2+1],
                         'y2': segment_data['y_mm'].iloc[iLines2+1]}
                lines_do_intersect, intersection = lt.linesIntersect(line1, line2)
                if(lines_do_intersect):
                    #calculate the distance between the start of line1 and the start of line2
                    #Although this is not precise I believe the error is insignificant and
                    #and that it is a waste of time calculating the length exactly
                    length = segment_data['CumulativeDistance'].iloc[iLines2] - \
                                segment_data['CumulativeDistance'].iloc[iLines1]
#                    TEST to see that it is finding loops correct
#                    fig, ax = plt.subplots( nrows=1, ncols=1 )
#                    ax.plot(self.segment_data['x'].iloc[iLines1:iLines2+2],self.segment_data['y'].iloc[iLines1:iLines2+2])   
#                    filename = "C:/Users/Mark/Desktop/Bees Project/Code/Testing/" + str(iLines1) + ".png"
#                    fig.savefig(filename) 
#                    plt.close(fig)
                    if(length > max_length):
                        #print("length:", length)
                        max_length = length
#                        ax.plot(self.segment_data['x'].iloc[iLines1:iLines2+2],self.segment_data['y'].iloc[iLines1:iLines2+2])   
#                        return(0)
        return(max_length)
        
        
class InnerRadiusVariation(Feature):
    
    def featureName(self):
        return "InnerRadiusVariation"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())      
        sg = self.segment
        
        points_distance_centre_ellipse = np.sqrt(np.square(sg.points[:,0]-sg.ellipse.centre[0]) + np.square(sg.points[:,1]-sg.ellipse.centre[1]))
        
        median = np.median(points_distance_centre_ellipse)
        UQ = np.percentile(points_distance_centre_ellipse, 75)   
        LQ =  np.percentile(points_distance_centre_ellipse, 25)
        
        inner_radius_variation = (UQ - LQ)/median
        #print("Inner radius variation:", inner_radius_variation)        
        
        return(inner_radius_variation)
        
class CentralDisplacement(Feature):
    
    def featureName(self):
        return "CentralDisplacement"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        ellipse_centre_x = self.segment.ellipse.centre[0]
        ellipse_centre_y = self.segment.ellipse.centre[1]
        
        x_distance = ellipse_centre_x-self.segment.arena.centre_x
        y_distance = ellipse_centre_y-self.segment.arena.centre_y
        
        central_displacement = np.sqrt(np.square(x_distance) + np.square(y_distance))*2/self.segment.arena.diameter
        
        return(central_displacement)
        

class MeanSpeed(Feature):
    
    def featureName(self):
        return "MeanSpeed"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        mean_speed = np.mean(self.segment.segment_data['Speed'].iloc[1:])        
        return(mean_speed)
        
class MedianSpeed(Feature):
    
    def featureName(self):
        return "MedianSpeed"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        median_speed = np.median(self.segment.segment_data['Speed'].iloc[1:])        
        return(median_speed)
        
class MinSpeed(Feature):
    
    def featureName(self):
        return "MinSpeed"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        min_speed = np.min(self.segment.segment_data['Speed'].iloc[1:])
        return(min_speed)
        
class MaxSpeed(Feature):
    def featureName(self):
        return "MaxSpeed"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        max_speed = np.max(self.segment.segment_data['Speed'].iloc[1:])
        return(max_speed)
        
class IQSpeed(Feature):
    def featureName(self):
        return "IQSpeed"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        UQ = np.percentile(self.segment.segment_data['Speed'].iloc[1:], 75)   
        LQ =  np.percentile(self.segment.segment_data['Speed'].iloc[1:], 25)
        IQR = (UQ - LQ)
        return(IQR)
        
class MeanRotation(Feature):
    
    def featureName(self):
        return "MeanRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        mean_rotation = np.mean(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(mean_rotation)
        
class MedianRotation(Feature):
    
    def featureName(self):
        return "MedianRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        median_rotation = np.median(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(median_rotation)
        
class MinRotation(Feature):
    
    def featureName(self):
        return "MinRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        min_rotation = np.min(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(min_rotation)

class MaxRotation(Feature):
    
    def featureName(self):
        return "MaxRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        max_rotation = np.max(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(max_rotation)
        
class IQRotation(Feature):
    def featureName(self):
        return "IQRotation"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        UQ = np.percentile(self.segment.segment_data['Rotation_Corrected'].iloc[1:], 75)   
        LQ =  np.percentile(self.segment.segment_data['Rotation_Corrected'].iloc[1:], 25)
        IQR = (UQ - LQ)
        return(IQR)
        
class MeanAbsRotation(Feature):
    
    def featureName(self):
        return "MeanAbsRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        mean_rotation = np.mean(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(mean_rotation)
        
class MedianAbsRotation(Feature):
    
    def featureName(self):
        return "MedianAbsRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        median_rotation = np.median(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(median_rotation)

class MinAbsRotation(Feature):
    
    def featureName(self):
        return "MinAbsRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        min_rotation = np.min(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(min_rotation)
        
class MaxAbsRotation(Feature):
    
    def featureName(self):
        return "MaxAbsRotation"

    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        max_rotation = np.max(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(max_rotation)
        
class IQAbsRotation(Feature):
    def featureName(self):
        return "IQAbsRotation"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        UQ = np.percentile(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:], 75)   
        LQ =  np.percentile(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:], 25)
        IQR = (UQ - LQ)
        return(IQR)
        
class PathEfficiency(Feature):
    def featureName(self):
        return "PathEfficiency"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        sg = self.segment.segment_data
        return(math.sqrt((sg['x_mm'].iloc[-1] - sg['x_mm'].iloc[0])**2 + (sg['y_mm'].iloc[-1] - sg['y_mm'].iloc[0])**2) / (sg['CumulativeDistance'].iloc[-1] - sg['CumulativeDistance'].iloc[0]))
        
class SumAbsoluteAngles(Feature):
    def featureName(self):
        return "SumAbsoluteAngles"
        
    def extractVector(self, sg, index):
#        print("sg.iloc[index + 1]['x_mm']: ", sg.iloc[index]['x_mm'])
#        print("sg.iloc[index + 1]['y_mm']: ", sg.iloc[index]['y_mm'])
        u =  {'x' : sg.iloc[index + 1]['x_mm'] - sg.iloc[index]['x_mm'],
              'y' : sg.iloc[index + 1]['y_mm'] - sg.iloc[index]['y_mm']}
        return u
        
    def Magnitude(self, vector):
        magnitude = math.sqrt((vector['x']**2 + vector['y']**2))
        return magnitude
        
    def crossProduct(self, u, v):
        cross_product = v['x'] * u['x'] + v['y'] * u['y']
        return(cross_product)
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        sg = self.segment.segment_data.drop_duplicates(subset=['x_mm', 'y_mm'])
        nPoints = sg.shape[0]
        
        sum_angles = 0
        
        for iPoint in range(0, nPoints - 2):
            
            u = self.extractVector(sg, iPoint)
            v = self.extractVector(sg, iPoint+1)
#            print("u:", u)
#            print("v:", v)
            #print("self.crossProduct(u, v) / (self.Magnitude(u) * self.Magnitude(v)):", self.crossProduct(u, v) / (self.Magnitude(u) * self.Magnitude(v)))
            if(self.Magnitude(u) * self.Magnitude(v) != 0):
                assert abs(self.crossProduct(u, v) / (self.Magnitude(u) * self.Magnitude(v))) < 1.00000000001, "the input to acos is unreasonably outside the domain"
                if self.crossProduct(u, v) / (self.Magnitude(u) * self.Magnitude(v))>1:
                    angle = 0
                elif self.crossProduct(u, v) / (self.Magnitude(u) * self.Magnitude(v))<-1:
                    angle = math.pi
                else:
                    angle = math.acos(self.crossProduct(u, v) / (self.Magnitude(u) * self.Magnitude(v)))
            else:
                angle = 0
            sum_angles = sum_angles + angle
        
        return(sum_angles)
            
class LocationDensity(Feature):
    def featureName(self):
        return "LocationDensity"
        
    def calculateFeature(self):
        if self.print_feature_names: logging.info("Calculating feature " + self.featureName())
        sg = self.segment.segment_data.drop_duplicates(subset=['x_mm', 'y_mm'])
        nPoints = sg.shape[0]
        sum_distance_all_points = 0
        
        for iStartPoint in range(0, nPoints - 1):
            for iEndPoint in range(iStartPoint + 1, nPoints):
                StartPoint = {'x': sg.iloc[iStartPoint]['x_mm'], 'y': sg.iloc[iStartPoint]['y_mm']}
                EndPoint =   {'x': sg.iloc[iEndPoint]['x_mm'], 'y': sg.iloc[iEndPoint]['y_mm']}
#                print("StartPoint:", StartPoint)
#                print("EndPoint:", EndPoint)
#                diff_x = EndPoint['x'] - StartPoint['x']

                sum_distance_all_points = sum_distance_all_points + \
                                math.sqrt((EndPoint['x'] - StartPoint['x'])**2 + (EndPoint['y'] - StartPoint['y'])**2)               
        ncombinations_distances = comb(N = nPoints, k = 2, exact=False)
        
        location_density = sum_distance_all_points / ncombinations_distances
        
        return(location_density)
        
#======================================================================================

#class PathEfficiency(Feature):
#    def featureName(self):
#        return "PathEfficiency"
#        
#    def calculateFeature
        

