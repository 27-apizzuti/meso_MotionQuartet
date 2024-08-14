"""Read BrainVoyager vmr and export nifti.
NOTE: First export --> improve brain extraction """


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = 'sub-04'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat'.format(SUBJ)

# Load nifti: whole hemisphere segmentation
# WM = os.path.join(STUDY_PATH, 'sub-01_WM_bvbabel.nii.gz')
# wm_file =  nb.load(os.path.join(STUDY_PATH, WM))
# wm_data = np.asarray(wm_file.dataobj)
#
# # Load mask
# GM = os.path.join(STUDY_PATH, '04_CorticalMask', 'sub-01_GM_bvbabel.nii.gz')
# gm_file =  nb.load(os.path.join(STUDY_PATH, GM))
# gm_data = np.asarray(gm_file.dataobj)

#// Sub-03
WMGM = os.path.join(STUDY_PATH, 'KenshuDataset', 'rim012_afterMC_native.nii')
wmgm_file =  nb.load(os.path.join(STUDY_PATH, WMGM))
wmgm_data = np.asarray(wmgm_file.dataobj)

# Load polished segmentation in ROI
BM = os.path.join(STUDY_PATH, '02_AdvSeg', 'sub-04_cereb_out_native.nii.gz')
csf =  nb.load(os.path.join(STUDY_PATH, BM))
csf_data = np.asarray(csf.dataobj)

#//
new_data = np.zeros(np.shape(wmgm_data))
# new_data[csf_data > 0] = 1
# new_data[gm_data > 0] = 3
# new_data[wm_data > 0] = 2
#

new_data[csf_data > 0] = 1
new_data[wmgm_data == 1] = 3
new_data[wmgm_data == 2] = 2


# Save nifti
outname = os.path.join(STUDY_PATH, 'KenshuDataset', '{}_RIM.nii.gz'.format(SUBJ))
img = nb.Nifti1Image(new_data, affine=np.eye(4))
nb.save(img, outname)
#
#
# # Save only GM
# new_data2 = np.zeros(np.shape(wmgm_data))
# new_data2[new_data == 3] = 1
#
# outname = os.path.join(STUDY_PATH, '{}_GM.nii.gz'.format(SUBJ))
# img = nb.Nifti1Image(new_data2, affine=np.eye(4))
# nb.save(img, outname)
