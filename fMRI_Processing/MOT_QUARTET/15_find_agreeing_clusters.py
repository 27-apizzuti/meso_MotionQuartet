"""Read BrainVoyager VMP and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
import matplotlib.pyplot as plt

SUB = 'sub-01'
hem = 'RH'

PATH_IN = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/'.format(SUB)

# Load t-map from ambiguous motion
FILENAME = '{}_Amb_maps_wholeBrain_bvbabel_res2x_float32.nii.gz'.format(SUB)
FILE = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Amb', FILENAME)

niimap = nb.load(FILE)
map_all = np.asarray(niimap.dataobj)

# Load ROI definition
ROIS_FILE = 'sub-01_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_V1.nii.gz'.format(hem)
rois_nii = nb.load(os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Phy', ROIS_FILE))
roi_data = np.asarray(rois_nii.dataobj)
idxh = roi_data == 1
idxv = roi_data == 2

#// Separate distributions
map = map_all[..., 0]
idx1 = map > 0
idx2 = map < 0

new_data = np.zeros(np.shape(roi_data))
new_data[idxh*idx1] = 1
new_data[idxv*idx2] = 2

print('Save clusters')
OUTPUTNAME = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Phy', '{}_amb_maps_wholeBrain_bvbabel_res2x_float32_consistent_clusters_{}.nii.gz'.format(SUB, hem))

img = nb.Nifti1Image(new_data, affine=niimap.affine, header=niimap.header)
nb.save(img, OUTPUTNAME)
