from dscribe.descriptors import MBTR
import os
import numpy as np
from os import listdir
from ase.io import read
import pandas as pd
import matplotlib.pyplot as plt
from figure import *
import pickle

def mbtr_func(element_list):
    mbtr_k2_grid_min = -0.1
    mbtr_k2_grid_max =1
    mbtr_k2_grid_n = 50
    mbtr_k2_grid_sigma = 0.02
    mbtr_k2_weight_scale = 1
    mbtr_k2_weight_cutoff = 1e-3
    mbtr = MBTR(
        species=['C', 'H', 'F', 'N', 'Ge', 'Sn', 'Cl', 'Br', 'Pb', 'O', 'I'],
        k2={
            "geometry": {"function": "inverse_distance"},
            "grid": {   "min":      mbtr_k2_grid_min,
                        "max":      mbtr_k2_grid_max, 
                        "sigma":    mbtr_k2_grid_sigma,
                        "n":        mbtr_k2_grid_n},
            "weighting": {  "function"  : "exp",
                            "scale"     : mbtr_k2_weight_scale,
                            "cutoff"    : mbtr_k2_weight_cutoff},
        },
        periodic=True,
    )
    return mbtr

maindir = './cif_files/'
subdirs = os.listdir((maindir))

mbtr = mbtr_func()
mbtr_all = []
for i in sorted(subdirs):
    if i.startswith('.DS_Store'):
        continue
    struc = read(maindir +  i)
    mbtr_all.append(mbtr.create(struc))

df_mbtr = pd.DataFrame(np.array(mbtr_all).reshape(1346,-1))

pickle.dump(df_mbtr, open('df_mbtr.pkl', 'wb'))