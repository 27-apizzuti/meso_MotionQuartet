"""Read BrainVoyager vmr and export nifti.
NOTE: First export --> improve brain extraction """


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = 'sub-03'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/'.format(SUBJ)

# Load nifti
# FILENAME = os.path.join(STUDY_PATH, '02_AvdSeg', '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_res2x.nii.gz'.format(SUBJ))
# FILENAME = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-03/derivatives/anat/02_AdvSeg/sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_res2x.nii.gz"
# print(FILENAME)
# nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
# nii_data = np.asarray(nii.dataobj)
#
# # Load mask
# # MASK = os.path.join(STUDY_PATH, '02_AvdSeg', '{}_subcorticalMask_native.nii.gz'.format(SUBJ))
# MASK = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-03/derivatives/anat/02_AdvSeg/sub-03_subcorticalMask_native.nii.gz"
# ma =  nb.load(os.path.join(STUDY_PATH, MASK))
# ma_data = np.asarray(ma.dataobj)
# nii_data[ma_data > 0] = 225
# # Save nifti
# outname = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-03/derivatives/anat/02_AdvSeg/sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_mask.nii.gz"
# # outname = os.path.join(STUDY_PATH, '02_AvdSeg', '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_mask.nii.gz'.format(SUBJ))
# img = nb.Nifti1Image(nii_data, affine=np.eye(4))
# nb.save(img, outname)

# Remove cerebellum

FILENAME = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat/01_SubcorticalMask/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_res2x.nii.gz"
print(FILENAME)
nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
nii_data = np.asarray(nii.dataobj)

MASK = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat/01_SubcorticalMask/sub-06_subcorticalMask_native_res2x.nii.gz"
ma =  nb.load(os.path.join(STUDY_PATH, MASK))
ma_data = np.asarray(ma.dataobj)
nii_data[ma_data > 0] = 225

outname = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat/01_SubcorticalMask/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x.nii.gz"
img = nb.Nifti1Image(nii_data, affine=np.eye(4))
nb.save(img, outname)
