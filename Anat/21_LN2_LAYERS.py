"Running LN2_LAYERS"

import nibabel as nb
import numpy as np
from time import time
import os
from glob import glob
import pathlib
import subprocess

# -----------------------------------
# USER's ENTRIES
SUBJ = ['sub-07']
NR_LAYERS = 3
for su in SUBJ:
    MAIN_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers'.format(su)
    # -----------------------------------
    # // Segmentation
    os.chdir(MAIN_PATH)
    rim_file =  glob("{}_RIM*.nii.gz".format(su))[0]
    print(rim_file)
    RIM = os.path.join(MAIN_PATH, '{}'.format(rim_file))

    # // Calling bash command
    # Determine output basename
    filename = RIM.split("/")[-1]
    basename, ext = filename.split(os.extsep, 1)
    outputname = os.path.join(MAIN_PATH, '{}_nr_layers3.nii.gz'.format(basename))

    print('LN2_LAYERS {}'.format(filename))

    command = "LN2_LAYERS "
    command += "-rim {} ".format(RIM)
    command += "-nr_layers {} -thickness -curvature ".format(NR_LAYERS)
    command += "-equivol "
    command += "-output {} ".format(outputname)
    subprocess.run(command, shell=True)
