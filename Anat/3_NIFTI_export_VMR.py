"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

# SUBJ = 'sub-01'
# STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat'.format(SUBJ)

# #// Reference VMR
# REF_VMR = os.path.join(STUDY_PATH, 'sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'.format(SUBJ))
# header, data = bvbabel.vmr.read_vmr(REF_VMR)
# print('Converting NIFTI to VMR')

# # Load nifti to convert
# FILENAME = 'sub-01_sess-02_acq-mp2rage_UNI_denoised_IIHC_res2x.nii.gz'.format(SUBJ)
# nii =  nb.load(os.path.join(STUDY_PATH, '03_SurfaceRecon', FILENAME))
# datanii = np.asarray(nii.dataobj)
# #
# # MAS =  nb.load(os.path.join(STUDY_PATH, '02_AdvSeg', 'standardBV', 'sub-04_subcortial_mask_bvbabel_native.nii.gz'))
# # dataniimas = np.asarray(MAS.dataobj)
# #
# # datanii[dataniimas > 0] = 225

# # idx1 = datanii == 47
# # idx2 = datanii == 35s
# #
# # new_data = np.zeros(np.shape(datanii))
# # new_data[idx1] = 1
# # new_data[idx2] = 1
# # datanii[datanii <0]=0
# # Save new vmr
# outname = os.path.join(STUDY_PATH, 'sub-01_sess-02_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'.format(SUBJ))
# bvbabel.vmr.write_vmr(outname, header, datanii)
#
# #// V16
# print('Converting NIFTI to V16')
# REF_V16 = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.v16'.format(SUBJ))

# # Load nifti
# FILENAME = '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_v16_bvbabel_SS.nii.gz'.format(SUBJ)
# nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
# datav16 = np.asarray(nii.dataobj)
#
# # Load ref V16
# outname = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS.v16'.format(SUBJ))
# header, data = bvbabel.v16.read_v16(REF_V16)
# bvbabel.v16.write_v16(outname, header, datav16)

# Quick and dirty 
REF_VMR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-10/derivatives/anat/sub-10_sess-01_acq-mp2rage_UNI.vmr"
NIFTI = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-10/derivatives/anat/test-sess-03/test.nii.gz"

# #// V16
print('Converting NIFTI to V16')
REF_V16 = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-10/derivatives/anat/sub-10_sess-01_acq-mp2rage_UNI.v16"
header, data = bvbabel.v16.read_v16(REF_V16)

# header, data = bvbabel.vmr.read_vmr(REF_VMR)
# print('Converting NIFTI to VMR')

# Load nifti to convert
nii =  nb.load(NIFTI)
datanii = np.asarray(nii.dataobj).astype(np.uint16)

outname = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-10/derivatives/anat/sub-10_sess-01_acq-mp2rage_UNI_aligned_sess-03.v16"
bvbabel.v16.write_v16(outname, header, datanii)