# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 13:32:56 2017

@author: Mark
"""

import classArena
import main
import pandas as pd
import logging
import os

from os import chdir, getcwd
wd=getcwd()
chdir(wd)
 
# add filemode="w" to overwrite

#initialisation
datapath = "../../Data/"

logging.basicConfig(filename=os.path.join(datapath, "sample.log"), level=logging.DEBUG, filemode = "w")

df_nt = pd.read_csv(datapath + "bee-data_NT.csv")
df_procaine = pd.read_csv(datapath + "bee-data_procaine.csv")
df_saline = pd.read_csv(datapath + "bee-data_saline.csv")

dfs_combined = pd.concat([df_nt, df_procaine, df_saline], axis=0)
temp_arena = classArena.classArena(dfs_combined)

#main.process_all_dfs(seg_length = 50, overlap = 0.7, folder_name = "length50",
#                data_folder_path = datapath, 
#                data_nt = df_nt, data_procaine = df_procaine, data_saline = df_saline, 
#                arena = temp_arena)

main.process_all_dfs(seg_length = 100, overlap = 0.7, folder_name = "length100",
                data_folder_path = datapath, 
                data_nt = df_nt, data_procaine = df_procaine, data_saline = df_saline, 
                arena = temp_arena)

#main.process_all_dfs(seg_length = 150, overlap = 0.7, folder_name = "length150",
#                data_folder_path = datapath, 
#                data_nt = df_nt, data_procaine = df_procaine, data_saline = df_saline, 
#                arena = temp_arena)
#                
#main.process_all_dfs(seg_length = 200, overlap = 0.7, folder_name = "length200",
#                data_folder_path = datapath, 
#                data_nt = df_nt, data_procaine = df_procaine, data_saline = df_saline, 
#                arena = temp_arena)
#                
#main.process_all_dfs(seg_length = 250, overlap = 0.7, folder_name = "length250",
#                data_folder_path = datapath, 
#                data_nt = df_nt, data_procaine = df_procaine, data_saline = df_saline, 
#                arena = temp_arena)

#main.process_all_dfs(seg_length = 300, overlap = 0.7, folder_name = "length300",
#                data_folder_path = datapath, 
#                data_nt = df_nt, data_procaine = df_procaine, data_saline = df_saline, 
#                arena = temp_arena)

logging.shutdown()