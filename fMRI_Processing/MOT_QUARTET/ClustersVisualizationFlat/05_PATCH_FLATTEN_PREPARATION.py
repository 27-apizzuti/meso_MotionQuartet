"""
Created on Thu Oct 28 14:21:14 2021
Patch Flattening script: anatomical images
NB: This script computes automatically the number of bin that should be used (x,y,z) once decided the "nominal (desired) resolution for the flattened domain"
Remeber to check the density file!!!
@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import subprocess
import math
from glob import glob

SUBJ = ['sub-01', 'sub-03', 'sub-06']
HEMI = ['LH', 'RH']
ROI = 'hMT'

for iterSbj, su in enumerate(SUBJ):
    PATH_EPI = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/Hyph01'.format(su)
    for hem in HEMI:
        VALUE = os.path.join(PATH_EPI, '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_UVD_max_filter_ambiguous_mask.nii.gz'.format(su, hem, ROI))
        # 1) Add 1 to mask
        print("Working on {}, adding 1 to {}".format(su, VALUE))
        output_name = os.path.join(PATH_EPI, '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_UVD_max_filter_ambiguous_mask_plus1.nii.gz'.format(su, hem, ROI))
        command = "fslmaths "
        command += "{} ".format(VALUE)
        command += "-add 1 "
        command += "{}".format(output_name)
        subprocess.run(command, shell=True)
