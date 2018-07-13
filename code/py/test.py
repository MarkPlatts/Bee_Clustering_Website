# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 06:33:50 2017

@author: Mark
"""

import unittest
import segment as sg
import preprocess
import loop_tool as lt
import math
import numpy as np
import create_segment as cs
import classArena
import enums
import pandas as pd

from os import chdir, getcwd
wd=getcwd()
chdir(wd)

class TestSegmentMethods(unittest.TestCase):
            
        
    def test_MaximumLoopLength(self):
        
        df = pd.read_csv("../../Data/TestData/bee-data_NT_test_maxloop.csv")
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df,20,0,0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena, index = 0)

        feat = features_first_segment.getFeature(enums.eFeature.MaximumLoop)    
        self.assertEqual(feat.value, 15)
        
    
    def test_FindingCorrectSecondSegment(self):      
        
        df = preprocess.execute("../../Data/TestData/bee-data_NT_test.csv")
        
        first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)

        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[0], 7.0969949712)
        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[-1], 17.5320477473)
        
    def test_DistancePoint100FromCentre(self):
        
        df = preprocess.execute(
        "../../Data/TestData/bee-data_NT_test.csv")
        
        Distance = df['DistanceCentre'].iloc[99]
        print("Distance:", Distance)
        self.assertAlmostEqual(Distance, 36.1062682861314)
        
    def test_MedianDistanceCentre(self):
        
        df = preprocess.execute(
        "../../Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)        
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        dt_second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)
        length_second_segment = cs.getSegmentLength(dt_second_segment)
        
        features_second_segment = sg.Segment(dt_second_segment, length_second_segment, arena, 0)
        
        feat = features_second_segment.getFeature(enums.eFeature.MedianDistanceFromCentre)    
        
        self.assertAlmostEqual(feat.value, 0.8628325515)
        
    def test_iQRangeDistanceCentre(self):
        df = preprocess.execute(
        "../../Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)        
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        dt_second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)
        
        len_second_segment = cs.getSegmentLength(dt_second_segment)        
        second_segment_features = sg.Segment(dt_second_segment, len_second_segment, arena, 0)
        
        feat = second_segment_features.getFeature(enums.eFeature.IQRange) 
        self.assertAlmostEqual(feat.value, 0.0164803959758471)

        
    def test_getSegmentLength(self):
        df = preprocess.execute(
        "../../Data/TestData/bee-data_NT_test.csv")

        first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment) 
        
        length_segment = cs.getSegmentLength(second_segment)
        
        self.assertAlmostEqual(length_segment, 10.4350527761)
        
    def test_areaFormula(self):
        df = preprocess.execute(
        "../../Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)        
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        dt_second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)
        length_second_segment = cs.getSegmentLength(dt_second_segment)
        
        features_second_segment = sg.Segment(dt_second_segment,length_second_segment, arena, 0)
        
        #features_second_segment.calcMinEnclosingEllipseArea

        points = np.array([[-1,0,0,1],[0,1,-1,0]]).T      
        
        ellipse = features_second_segment.findMinEnclosingEllipse(points)
        min_enclosing_ellipse_area = features_second_segment.calcMinEnclosingEllipseArea(ellipse.radii)
        
        self.assertAlmostEqual(min_enclosing_ellipse_area, math.pi)
        
    def test_LinesIntersect(self):        
        #See Intersect_Tests.jpg for what the letters refer to
        
        #A
        line1 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        line2 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #B
        line1 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        line2 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #C
        line1 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        line2 = {'x1': 2, 'y1': 1, 'x2': 1, 'y2': 2}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})

        #D
        line1 = {'x1': 2, 'y1': 1, 'x2': 1, 'y2': 2}
        line2 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #E
        line1 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        line2 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #F
        line1 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        line2 = {'x1': 2, 'y1': 1, 'x2': 1, 'y2': 2}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #G
        line1 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        line2 = {'x1': 4, 'y1': 2, 'x2': 3, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertFalse(bIntersect) 
        
        #H
        line1 = {'x1': 1, 'y1': 3, 'x2': 2, 'y2': 4}
        line2 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertFalse(bIntersect) 
        
        #I Unnecessary

        #J Overlapping
        line1 = {'x1': 1, 'y1': 1, 'x2': 3, 'y2': 3}
        line2 = {'x1': 2, 'y1': 2, 'x2': 4, 'y2': 4}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 2.0, 'y': 2.0})
        
        #K same gradient but not overlapping
        line1 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        line2 = {'x1': 3, 'y1': 3, 'x2': 4, 'y2': 4}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertFalse(bIntersect)         
        
    def test_calcCentralDisplacement_withinCorrectRange(self): 
        
        df = preprocess.execute(
        "../../Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)
        
        dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)
        for i in range(0,20):
            dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment) 
            length_segment = cs.getSegmentLength(dt_segment)
            features_segment = sg.Segment(dt_segment, length_segment, arena, 0)
            cent_displ = features_segment.getFeature(enums.eFeature.CentralDisplacement).value
#            print("cent_displ:", cent_displ)
            self.assertLessEqual(cent_displ, 1) # test never bigger than arena size
            self.assertGreater(cent_displ, 0) # test positive
            self.assertGreaterEqual(cent_displ, (features_segment.ellipse.centre[0] - arena.centre_x) * 2 / arena.diameter) # test greater than ellipse centre x
            self.assertGreaterEqual(cent_displ, (features_segment.ellipse.centre[1] - arena.centre_y) * 2 / arena.diameter) # test greater than ellipse centre y

    def test_calcMeanSpeed(self):

        df = preprocess.execute("../../Data/TestData/bee-data_NT_test_maxloop.csv")
                                                                #(traj, lseg, ovlp, cum_dist_end_prev)
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df,20,0,0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena, 0)
        
        feat = features_first_segment.getFeature(enums.eFeature.MeanSpeed)      

        self.assertEqual(feat.value, 118.75)

    def test_checkCorrectingRotation(self):
      
        df = preprocess.execute("../../Data/TestData/bee-data_NT_test_maxloop.csv")
                                                                #(traj, lseg, ovlp, cum_dist_end_prev)
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df,20,0,0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena, 0)
        
        feat = features_first_segment.getFeature(enums.eFeature.MeanSpeed)      

        self.assertEqual(feat.value, 118.75)
        
    def test_pathEfficiency(self):
        
        df = preprocess.execute("../../Data/TestData/bee-data_NT_test_sum_abs_angles.csv")
                                                                #(traj, lseg, ovlp, cum_dist_end_prev)
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df,20,0,0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena, 0)
        
        feat = features_first_segment.getFeature(enums.eFeature.PathEfficiency)  
        
        PathEfficiency_TrueValue = 1.0/7.0

        self.assertEqual(feat.value, PathEfficiency_TrueValue)

#    def test_output_to_csv(self):
#        
#        df = preprocess.execute(
#        "../../Data/TestData/bee-data_NT_test.csv")
#        arena = classArena.classArena(df)
#        
#        dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)
#        list_segments = None
#        for i in range(0,20):
#            dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment) 
#            length_segment = cs.getSegmentLength(dt_segment)
#            list_segments = [list_segments, sg.Segment(dt_segment, length_segment, arena)]
            
    def test_sumAbsAngles(self):
                                 
        df = preprocess.execute("../../Data/TestData/bee-data_NT_test_sum_abs_angles.csv")
                                                                #(traj, lseg, ovlp, cum_dist_end_prev)
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 7, 0, 0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena, 0)
        
        feat = features_first_segment.getFeature(enums.eFeature.SumAbsoluteAngles)      

        self.assertEqual(feat.value, 2 * math.pi)  
        
    def test_locationDensity(self):
        
        df = preprocess.execute("../../Data/TestData/bee-data_NT_test_locationDensity.csv")
                                                                #(traj, lseg, ovlp, cum_dist_end_prev)
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 7, 0, 0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena, 0)
        
        feat = features_first_segment.getFeature(enums.eFeature.LocationDensity)   
        
        SumDistanceBetweenEachPairPoints = 1 + math.sqrt(1**2 + 2**2) + 2 \
                                            + 2 + math.sqrt(1**2 + 2**2) \
                                            + 1
                                            
        nCr = 6
        
        LocationDensity_TrueValue = SumDistanceBetweenEachPairPoints / nCr

        self.assertEqual(feat.value, LocationDensity_TrueValue)         
        
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestSegmentMethods)
unittest.TextTestRunner(verbosity=2).run(suite)