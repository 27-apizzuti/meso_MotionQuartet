"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from copy import copy

SUBJ = 'sub-01'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/'.format(SUBJ)

#// LOAD VMR
REF_VMR = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'.format(SUBJ))
header, data = bvbabel.vmr.read_vmr(REF_VMR)

#// LOAD NIFTI
HEM = 'RH'
TAG = 'stimulus_reconstructed'   # stimulus_reconstructed // visual_areas_hMT
FILENAME = '{}_{}_{}_bvbabel_rim_cortMask_voronoi_noCapsule.nii.gz'.format(SUBJ,TAG,  HEM)
nii =  nb.load(os.path.join(STUDY_PATH, '05_ROI_seg', 'voronoi', 'voi', FILENAME))
datanii = np.asarray(nii.dataobj)

#// lOAD VOI (as reference for the header.)
VOI = os.path.join(STUDY_PATH, '04_CorticalMask', '{}_{}_{}.voi'.format(SUBJ, TAG, HEM))
voi_header, data_voi = bvbabel.voi.read_voi(VOI)
nmap = voi_header['NrOfVOIs']

#// Change datanii array to match VOI
new_data = np.zeros(np.shape(datanii))
new_data = copy(datanii)
new_data = new_data[::-1,::-1, ::-1]
new_data = np.transpose(new_data, (1, 2, 0))

for it in range(0, nmap):
    # Loop over each ROI (different number and put it back)
    idx_voxels = np.argwhere(new_data == it+1)
    print(data_voi[it])
    data_voi[it]["NrOfVoxels"] = idx_voxels.shape[0]
    data_voi[it]["Coordinates"] = idx_voxels
#
outname = os.path.join(STUDY_PATH, '05_ROI_seg', 'voronoi', 'voi','{}_{}_{}_bvbabel_rim_cortMask_voronoi_noCapsule.voi'.format(SUBJ, TAG, HEM))
bvbabel.voi.write_voi(outname, voi_header, data_voi)
#
print("Finished.")
