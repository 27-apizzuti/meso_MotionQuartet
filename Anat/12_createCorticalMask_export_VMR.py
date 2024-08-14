"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = 'sub-01'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/'.format(SUBJ)

REF_VMR = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'.format(SUBJ))
header, data = bvbabel.vmr.read_vmr(REF_VMR)

#// VMR
print('Converting NIFTI to VMR')

# Load nifti
FILENAME = '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_mask_ETC-7x-R5_v-03_GM_bvbabel.nii.gz'.format(SUBJ)
nii =  nb.load(os.path.join(STUDY_PATH, '04_CorticalMask', FILENAME))
data = np.asarray(nii.dataobj)

FILENAME = '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_mask_ETC-7x-R5_v-03_GM_bvbabel.nii.gz'.format(SUBJ)
nii =  nb.load(os.path.join(STUDY_PATH, '04_CorticalMask', FILENAME))
data = np.asarray(nii.dataobj)


# Load ref vmr

outname = os.path.join(STUDY_PATH, '03_SurfaceRecon', '{}_WM_RH_polished_v-03.vmr'.format(SUBJ))
bvbabel.vmr.write_vmr(outname, header, datavmr)
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
