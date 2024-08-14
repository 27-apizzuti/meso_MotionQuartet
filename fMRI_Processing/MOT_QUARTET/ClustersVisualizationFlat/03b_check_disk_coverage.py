"""
Created on Thu Oct 28 14:21:14 2021
Evaluating "disk" coverage: how many activated voxels fit into the disk / total number of initial voxels
Activity volume computation.
Percentage of activity volume covered by the disk
NOTE: Quality check
@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import subprocess
from glob import glob

SUBJ = ['sub-06']
MAIN_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'
ROI = 'V1'
HEMI = 'RH'
vox_vol = 0.35 * 0.35 * 0.35
# ------------------------------------------------------------------------------
# Execute
for iterSbj, su in enumerate(SUBJ):
    
    # Load perimeter chunck
    LAY_PATH = os.path.join(MAIN_PATH, su, 'derivatives', 'anat', '06_Multilaterate', '{}_{}'.format(ROI, HEMI))
    print(LAY_PATH)

    per_file =  glob(os.path.join(LAY_PATH, '*perimeter_chunk.*'))[0]
    print(per_file)
    niiper = nb.load(os.path.join(LAY_PATH, per_file))
    per_data = np.asarray(niiper.dataobj)
    idx1 = per_data > 0

    # Load physical clusters
    PATH_IN = os.path.join(MAIN_PATH, su, 'derivatives', 'func', 'Stats', 'Clusters-maxFilter')
    FILENAME = '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}.nii.gz'.format(su, HEMI, ROI)
    niimap = nb.load(os.path.join(PATH_IN, FILENAME))
    map_all = np.asarray(niimap.dataobj)
    idx2 = map_all > 0
    print(vox_vol)
    # Activation volume in gray matter
    nvox = np.sum(idx2)
    vol = nvox*vox_vol
    print("For {}, {} {}, activation volume: {:.3f} mm3".format(su, ROI, HEMI, vol/1000))

    # Disk coverage
    coverage = np.sum(idx1 * idx2)
    print("Disk coverage: {:.1f}%".format((coverage/nvox)*100))
