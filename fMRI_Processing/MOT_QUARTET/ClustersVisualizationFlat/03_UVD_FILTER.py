"Running LN2_UVD_FILTER"

import nibabel as nb
import numpy as np
from time import time
import os
from glob import glob
import pathlib
import subprocess

# -----------------------------------
# USER's ENTRIES
SUBJ = ['sub-07', 'sub-08']

HEM = ['RH']
ROI = ['hMT', 'V1']
RADIUS = 0.39
HEIGHT = 2
# -----------------------------------
for su in SUBJ:
    MAIN_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers'.format(su)
    FUNC_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/Clusters-maxFilter'.format(su)
    for ro in ROI:
        for hemi in HEM:
            # // VScalar map to propagate
            val_file = '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}.nii.gz'.format(su, hemi, ro)
            VALUES = os.path.join(FUNC_PATH, '{}'.format(val_file))

            # Find input file
            os.chdir(MAIN_PATH)
            uv_file =  glob("*{}_{}_UV_coordinates.*".format(ro, hemi))[0]
            d_file = glob("*metric_equivol.*")[0]
            dom_file = glob("*{}_{}_perimeter_chunk.*".format(ro, hemi))[0]

            #// Coordinates
            COORD_UV = os.path.join(MAIN_PATH, '{}'.format(uv_file))
            COORD_D = os.path.join(MAIN_PATH, '{}'.format(d_file))

            #// Domain
            DOMAIN = os.path.join(MAIN_PATH, '{}'.format(dom_file))

            # // Calling bash command
            # Determine output basename
            filename = val_file.split("/")[-1]
            basename, ext = filename.split(os.extsep, 1)
            outputname = os.path.join(FUNC_PATH, '{}'.format(basename))

            print('LN2_UVD_FILTER {}'.format(filename))

            command = "LN2_UVD_FILTER "
            command += "-values {} ".format(VALUES)
            command += "-coord_uv {} ".format(COORD_UV)
            command += "-coord_d {} ".format(COORD_D)
            command += "-domain {} ".format(DOMAIN)
            command += "-max -radius {} -height {} ".format(RADIUS, HEIGHT)
            command += "-output {} ".format(outputname)

            subprocess.run(command, shell=True)
