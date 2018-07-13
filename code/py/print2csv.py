# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:19:06 2017

@author: Mark
"""

import csv
import os.path


#Create CSV file

#def print2CSV(list_segments):
def output(list_segments, filepath):
    
    seg1 = list_segments[0] # This is only the first segment
    
    if not os.path.isfile(os.path.join(filepath, "segment_features.csv")):
        
        #create new file
        ofile = open(os.path.join(filepath, "segment_features.csv"), "wb")
        writer = csv.writer(ofile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        
        #write the column headers
        row = ["SegmentID", "Experiment", "UsingLight", "FileName"]
        for iFeature in seg1.features:
            row = row + [iFeature.featureName()]
        writer.writerow(row)    
        
    else:
        #connect to existing file
        ofile = open(os.path.join(filepath, "segment_features.csv"), "ab")
        writer = csv.writer(ofile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)     
    
    #write the segment values    
    for iSeg in list_segments:
        row = [iSeg.segmentID, iSeg.experiment_name, iSeg.using_light, iSeg.filename]
        for iFeature in iSeg.features:
            row = row + [iFeature.value]
        writer.writerow(row)
    
    ofile.close()

def output_xy(list_segments, filepath):

    if not os.path.isfile(os.path.join(filepath,"segment_xys.csv")):
        
        ofile = open(os.path.join(filepath,"segment_xys.csv"), "wb")
        writer = csv.writer(ofile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        
        row = ["SegmentID", "Experiment", "UsingLight", "FileName", "x_mm", "y_mm"]
        
        writer.writerow(row)    
        
    else:
        ofile = open(os.path.join(filepath,"segment_xys.csv"), "ab")
        writer = csv.writer(ofile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL) 
    
    #write the segment xys    
    for iSeg in list_segments:
        nRows = len(iSeg.segment_data.index)
        for iRow in range(0, nRows):
            row = [iSeg.segmentID, iSeg.experiment_name, iSeg.using_light, iSeg.filename, \
                    iSeg.segment_data.iloc[iRow]['x_mm'], iSeg.segment_data.iloc[iRow]['y_mm']]
            writer.writerow(row)
    
    ofile.close()    