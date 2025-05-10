from itertools import combinations
import photometry as pho
import inversion as inv
import geometry as geo
import pandas as pd
import numpy as np
import glob as gl

folder_path = "/home/tenet/Documents/thesis/scripts/photometry/esa/data2"

"""
observer_lat_range = (-180,180)
target_position = (5,26)
light_position = (0.01,0)
args = (observer_lat_range, target_position, light_position)

geo.geometry(*args, path_s=folder_path+"/geometry", id="A5")
"""

""" 
w_list = [0.3,0.9]
bc_list = [[0.3, 0.9], [0.3, 0.5], [0.9, 0.1]]
dzeta_list = [0, 30]
h_list = [0.5]
b0_list = [0.5]

args = (w_list, bc_list, dzeta_list, h_list, b0_list)

geometries = gl.glob(folder_path+"/geometry/A*.npz")
for i in range (1,6):
    fles = list(combinations(geometries, i))
    print(i, " done")
    for fle in fles:
        pho.photometry(*args, path_r=fle, path_s=folder_path+"/photometry")
"""

"""
for fle in gl.glob(folder_path+"/photometry/*.npz"):
    inv.inversion(path_r=fle, path_si=folder_path+"/inversion", path_sr=folder_path+"/results")
"""