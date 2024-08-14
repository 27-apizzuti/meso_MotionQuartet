"""Read BrainVoyager vmr and export nifti.
NOTE: First export --> improve brain extraction """


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = 'sub-01'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/'.format(SUBJ)
HEMI = 'RH'

# Load nifti: whole hemisphere segmentation
FILENAME = os.path.join(STUDY_PATH, '03_SurfaceRecon', '{}_WM_{}_polished.nii.gz'.format(SUBJ, HEMI))
nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
nii_data = np.asarray(nii.dataobj)

# Load mask
MASK = os.path.join(STUDY_PATH, '03_SurfaceRecon', '{}_visual_buble.nii.gz'.format(HEMI))
ma =  nb.load(os.path.join(STUDY_PATH, MASK))
ma_data = np.asarray(ma.dataobj)

# Load polished segmentation in ROI
SEG = os.path.join(STUDY_PATH, '03_SurfaceRecon', '{}_WM_{}_polished_edits.nii.gz'.format(SUBJ, HEMI))
seg =  nb.load(os.path.join(STUDY_PATH, SEG))
seg_data = np.asarray(seg.dataobj)

nii_data[ma_data == 1] = seg_data[ma_data == 1]

# Save nifti
outname = os.path.join(STUDY_PATH, '03_SurfaceRecon', '{}_WM_{}_polished_v-03.nii.gz'.format(SUBJ, HEMI))
img = nb.Nifti1Image(nii_data, affine=np.eye(4))
nb.save(img, outname)
