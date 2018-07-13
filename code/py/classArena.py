# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 08:23:58 2017

@author: Mark
"""


class classArena:
    """Arena Object
    
    Takes a dataset for the bee experiment and estimates the properties and
    dimensions of the arena.
    
    Parameters
    ----------
    data : pandas
        A dataset containing the x_mm and y_mm coordinates of the bees
        trajectory.

    Attributes
    ----------
    width : float
        The estimated width of the arena.
    height : float
        The estimated height of the arena.
    diameter : float
        The estimated diameter of the arena.  
        
    """
    
    def __init__(self, data):
        
        self.width = data[['x_mm']].max() - data[['x_mm']].min()
        self.height = data[['y_mm']].max() - data[['y_mm']].min()
        self.diameter = max(self.width.iloc[0], self.height.iloc[0])
        
        self.centre_x, self.centre_y = self.centreArena(data)

#        self.centre_x = (data[['x_mm']].max() + data[['x_mm']].min())/2
#        self.centre_y = (data[['y_mm']].max() + data[['y_mm']].min())/2

    def centreArena(self, df):
        """Estimates the location of the centre of the arena"""        
        
        centre_x = (df['x_mm'].max() + df[['x_mm']].min()).iloc[0]/2.0
        centre_y = (df['y_mm'].max() + df[['y_mm']].min()).iloc[0]/2.0
        return centre_x, centre_y