# -*- coding: utf-8 -*-
"""
Created on Tue May 09 16:10:35 2017

@author: Mark
"""

import matplotlib.pyplot as plt
import math
import classArena
import pandas as pd
import os
    
def drawArena(df):
    
    #lets say diameter is rounded up
    height = df[['y_mm']].max() - df[['y_mm']].min()
    width = df[['x_mm']].max() - df[['x_mm']].min()
    arena = classArena.classArena(df)
    
    circumference_x = []
    circumference_y = []
    
    for iDegree in range(1, 360+1):
        a = arena.centre_x
        b = arena.centre_y
        radians = iDegree/360.0 * 2 * math.pi
        x = a + width.iloc[0]/2.0*math.cos(radians)
        y = b + height.iloc[0]/2.0*math.sin(radians)
        circumference_x.append(x) 
        circumference_y.append(y)
        
    plt.plot(circumference_x, circumference_y)


def plot_segment(seg):
    
    plt.plot(seg['x_mm'], seg['y_mm'])
    
def load_df_for_arena_dims():
    df_nt = pd.read_csv(os.path.join("../../Data/bee-data_NT.csv"))
    df_procaine = pd.read_csv(os.path.join("../../Data/bee-data_procaine.csv"))
    df_saline = pd.read_csv(os.path.join("../../Data/bee-data_saline.csv"))
    x = pd.concat([df_nt, df_procaine, df_saline], axis=0)
    return(x)
    
#df_plot_arena: this is used to find the dimensions of the arena so it can be plotted
def plot_all(df_plot_arena, seg, index, n_rows, n_cols, title): 
    
    plt.subplot(n_rows, n_cols, index)
    
    font = {'weight' : 'normal',
        'size'   : 12}
    plt.title(title, **font)
    plt.axis('off')
    
    drawArena(df_plot_arena)
    
    plot_segment(seg)
    
    
    
    