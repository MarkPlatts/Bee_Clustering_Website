# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:50:35 2017

@author: Mark
"""

def verticalLineIntersect(lineVertical, lineB, lineBGradient):
    if(lineVertical['x1']>=lineB['x1'] and lineVertical['x1']<=lineB['x2']):
        lineB_y_intersect = calcYAxisIntersect(lineB, lineBGradient)    
        lineB_y_at_vertical_x = lineBGradient*lineVertical['x1'] + lineB_y_intersect
        if lineB_y_at_vertical_x >= lineVertical['y1'] and lineB_y_at_vertical_x <= lineVertical['y2']:
            intersection = {'x': lineVertical['x1'], 'y': lineB_y_at_vertical_x}
            return True, intersection
        else:
            return False, None
    else:
        return False, None
            
def verticalLinesOverlap(line1, line2):
    if (max(line1['y1'],line1['y2']>=min(line2['y1'],line2['y2']))) and (max(line2['y1'],line2['y2']>=min(line1['y1'],line1['y2']))):
        y_lower = max(line1['y1'], line2['y1'])
        y_upper = min(line1['y2'], line2['y2'])
        mid_point = (y_lower+y_upper)/2
        intersection = {'x': line1['x1'], 'y': mid_point}
        return True, intersection
    else:
        return False, None

def linesIntersect(line1, line2):
    line1 = reorientLineCoords(line1)
    line2 = reorientLineCoords(line2)
    
    convertLinesToFloat(line1)
    convertLinesToFloat(line2)
    
    line1_gradient = calcGradientLine(line1)
    line2_gradient = calcGradientLine(line2)
    
    if line1_gradient == float('inf') and line2_gradient != float('inf'): #line 1 is vertical
        doesIntersect, intersection = verticalLineIntersect(line1, line2, line2_gradient)
        return doesIntersect, intersection
    elif line1_gradient != float('inf') and line2_gradient == float('inf'): #line 2 is vertical
        doesIntersect, intersection = verticalLineIntersect(line2, line1, line1_gradient)
        return doesIntersect, intersection
    elif line1_gradient == float('inf') and line2_gradient == float('inf'):
        if line1['x1'] != line2['x1']:
            return False, None
        else:
            doesIntersect, intersection = verticalLinesOverlap(line1, line2)
            return(doesIntersect, intersection)
    else:
        line1_y_intersect = calcYAxisIntersect(line1, line1_gradient)
        line2_y_intersect = calcYAxisIntersect(line2, line2_gradient)
        
        #check if gradient of each line is equal
        if line1_gradient==line2_gradient:
            
            #if gradient is equal check if lines overlap
            max_lower_x = max(line1['x1'], line2['x2'])
    
            line1_calc_y_at_max_lower_x = line1_gradient * max_lower_x + line1_y_intersect
            line2_calc_y_at_max_lower_x = line2_gradient * max_lower_x + line2_y_intersect
            if(line1_calc_y_at_max_lower_x==line2_calc_y_at_max_lower_x):                
                #if lines overlap return does cross and midpoint x,y of line1
                intersection = {'x': (line1['x1'] + line1['x2'])/2, 'y': (line1['y1'] + line1['y2'])/2}
                if(intersectsWithinBothLinesRange(intersection['x'], line1, line2)):
                    return True, intersection
                else:
                    return False, None
            else:
                return False, None
        elif(line1_gradient!=line2_gradient):
            #if gradient is not equal find x,y values at which they overlap
            intersection = findIntersect(line1_gradient, line1_y_intersect, line2_gradient, line2_y_intersect)
            
            #check if x value is within overlapping x range for each line
            if(intersectsWithinBothLinesRange(intersection['x'], line1, line2)):
                return True, intersection
            else:
                return False, None
                
def reorientLineCoords(line):
    #lines are represented by two sets of coordinates
    #this routine swaps the coordinates if the second x value is less than the first
    #effectively pointing the line from left to right
    #not sure this is necessary but did it because I know that code to check intersection
    #will work if I do this
    
    if(line['x1']<line['x2']):
        return(line)
    else:
        temp_min_x = line['x2']
        temp_min_y = line['y2']
        temp_max_x = line['x1']
        temp_max_y = line['y1']
        line['x1'] = temp_min_x
        line['y1'] = temp_min_y
        line['x2'] = temp_max_x
        line['y2'] = temp_max_y
        return(line)
        
def findIntersect(gradient1, intersect1, gradient2, intersect2):
    x = (intersect2 - intersect1)/(gradient1 - gradient2)
    y = gradient1*x + intersect1
    return {'x':x, 'y':y}
    
def intersectsWithinBothLinesRange(x, line1,line2):
    max_lower_x = max(line1['x1'], line2['x1'])
    min_upper_x = min(line1['x2'], line2['x2'])
    return(x>=max_lower_x and x<=min_upper_x)   
    
def convertLinesToFloat(line):
    line['x1'] = float(line['x1'])
    line['x2'] = float(line['x2'])
    line['y1'] = float(line['y1'])
    line['y2'] = float(line['y2'])
        
def calcGradientLine(line):
    if(line['x2']-line['x1']==0): #the line is vertical and gradient would be infinite
        return float('inf')
    else:
        return(line['y2']-line['y1']) / (line['x2']-line['x1'])
    
def calcYAxisIntersect(line, gradient):
    return(line['y1'] - gradient * line['x1'])