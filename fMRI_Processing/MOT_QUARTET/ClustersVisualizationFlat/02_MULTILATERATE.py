"Running LN2_MULTILATERATE"

import nibabel as nb
import numpy as np
from time import time
import os
from glob import glob
import pathlib
import subprocess

# -----------------------------------
# USER's ENTRIES
SUBJ = 'sub-08'
MAIN_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/05_CorticalLayers'.format(SUBJ)
RADIUS = 80
HEM = 'RH'
ROI = 'V1'

# // Segmentation & control point
if SUBJ == 'sub-01':
    rim_file = 'sub-01_RIM_masked_v-05_polished.nii.gz'
    cp_file = 'sub-01_RIM_masked_v-05_polished_nr_layers3_midGM_equidist_control_point_{}_{}.nii.gz'.format(ROI, HEM)
if SUBJ == 'sub-03':
    rim_file = 'sub-03_RIM_masked_v03_polished_edit3_polished_polished.nii.gz'
    cp_file = 'sub-03_RIM_masked_v03_polished_edit3_polished_polished_nr_layers3_midGM_equidist_control_point2_{}_{}.nii.gz'.format(ROI, HEM)
if SUBJ == 'sub-06':
    rim_file = 'sub-06_RIM_ZOOM_v-03_polished.nii.gz'
    cp_file = 'sub-06_RIM_ZOOM_v-03_polished_nr_layers3_midGM_equidist_control_point_{}_{}.nii.gz'.format(ROI, HEM)
if SUBJ == 'sub-04':
    rim_file = 'sub-04_RIM_ZOOM_v02_polished.nii.gz'
    cp_file = 'sub-04_RIM_ZOOM_v02_polished_nr_layers3_midGM_equidist_control_point_{}_{}.nii.gz'.format(ROI, HEM)
if SUBJ == 'sub-07':
    rim_file = 'sub-07_RIM_polished_mas_v-03_polished.nii.gz'
    cp_file = 'sub-07_RIM_polished_mas_v-03_polished_nr_layers3_midGM_equidist_control_point_{}_{}.nii.gz'.format(ROI, HEM)
if SUBJ == 'sub-08':
    rim_file = 'sub-08_RIM_polished_mas_polished.nii.gz'
    cp_file = 'sub-08_RIM_polished_mas_polished_nr_layers3_midGM_equidist_control_point_{}_{}.nii.gz'.format(ROI, HEM)
if SUBJ == 'sub-09':
    rim_file = 'sub-09_RIM_polished_mas_v-02_polished.nii.gz'
    cp_file = 'sub-09_RIM_polished_mas_v-02_polished_nr_layers3_midGM_equidist_control_point_{}_{}.nii.gz'.format(ROI, HEM)

if SUBJ == 'sub-10':
    rim_file = 'sub-10_RIM_polished_mas_polished.nii.gz'
    cp_file = 'sub-10_RIM_polished_mas_polished_nr_layers3_midGM_equidist_control_point_{}_{}.nii.gz'.format(ROI, HEM)

# -----------------------------------
RIM = os.path.join(MAIN_PATH, '{}'.format(rim_file))
CP = os.path.join(MAIN_PATH, '{}'.format(cp_file))

# // Calling bash command
# Determine output basename
filename = RIM.split("/")[-1]
basename, ext = filename.split(os.extsep, 1)
outputname = os.path.join(MAIN_PATH, '{}_radius_{}_{}_{}.nii.gz'.format(basename, RADIUS, ROI, HEM))

print('LN2_MULTILATERATE {}'.format(filename))

command = "LN2_MULTILATERATE "
command += "-rim {} ".format(RIM)
command += "-radius {} ".format(RADIUS)
command += "-control_points {} ".format(CP)
command += "-output {} ".format(outputname)
subprocess.run(command, shell=True)
