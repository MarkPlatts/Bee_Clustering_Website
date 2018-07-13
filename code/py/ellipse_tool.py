# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 15:43:34 2017

@author: Mark
"""

from __future__ import division
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#import sys
import numpy as np
from numpy import linalg
#from random import random
#import math


class EllipseTool:
    """Some stuff for playing with ellipsoids"""
    def __init__(self):
        self.centre = None
        self.radii = None
        self.rotation = None
        
    
    def calcMinAreaEllipse(self, P=None, tolerance=0.01):
        #Taken from https://github.com/minillinim/ellipsoid/blob/master/ellipsoid.py and altered so
        #that it works with ellipses in 2d - (mark platts 7/3/17)        
        
        """ Find the minimum volume ellipsoid which holds all the points
        
        Based on work by Nima Moshtagh
        http://www.mathworks.com/matlabcentral/fileexchange/9542
        and also by looking at:
        http://cctbx.sourceforge.net/current/python/scitbx.math.minimum_covering_ellipsoid.html
        Which is based on the first reference anyway!
        
        Here, P is a numpy array of N dimensional points like this:
        P = [[x,y,z,...], <-- one point per line
             [x,y,z,...],
             [x,y,z,...]]
        
        Returns:
        (centre, radii, rotation)
        
        """
        (N, d) = np.shape(P)
        d = float(d)
    
        # Q will be our working array
        Q = np.vstack([np.copy(P.T), np.ones(N)]) 
        QT = Q.T
        
        # initializations
        err = 1.0 + tolerance
        u = (1.0 / N) * np.ones(N)

        # Khachiyan Algorithm
        while err > tolerance:
            V = np.dot(Q, np.dot(np.diag(u), QT))
            M = np.diag(np.dot(QT , np.dot(linalg.inv(V), Q)))    # M the diagonal vector of an NxN matrix
            j = np.argmax(M)
            maximum = M[j]
            step_size = (maximum - d - 1.0) / ((d + 1.0) * (maximum - 1.0))
            new_u = (1.0 - step_size) * u
            new_u[j] += step_size
            err = np.linalg.norm(new_u - u)
            u = new_u

        # centre of the ellipse 
        self.centre = np.dot(P.T, u)
    
        # the A matrix for the ellipse
        A = linalg.inv(
                       np.dot(P.T, np.dot(np.diag(u), P)) - 
                       np.array([[a * b for b in self.centre] for a in self.centre])
                       ) / d
                       
        # Get the values we'd like to return
        U, s, self.rotation = linalg.svd(A)
        self.radii = 1.0/np.sqrt(s)
        
        pass
        #return (centre, radii, rotation) # centre(x,y)
        
        
    def getEllipseArea(self, radii):
        """Calculate the volume of the blob"""
        return np.pi*radii[0]*radii[1]