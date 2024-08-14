"""Read BrainVoyager vmr and export nifti.
NOTE: This script is used multiple times during the anatomical pipeline
e.g. export 1) brainmask 2) subcortical mask 3) WM 4) GM"""


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = 'sub-04'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/02_AdvSeg'.format(SUBJ)

# VMR
FILENAME = 'sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_BFC_STEDI_n10_s0pt5_r2pt0_g1_mask_ETC-7x-R5_WM_GM.vmr'
FILE = os.path.join(STUDY_PATH, FILENAME)
header, data = bvbabel.vmr.read_vmr(FILE)

# Export nifti
basename = FILENAME.split(os.extsep, 1)[0]
outname = os.path.join(STUDY_PATH, "{}_bvbabel.nii.gz".format(basename))
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)
# # #
# # V16
# FILENAME = 'sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC.v16'
# FILE = os.path.join(STUDY_PATH, FILENAME)
# header, data = bvbabel.v16.read_v16(FILE)
#
# # Export nifti
# basename = FILENAME.split(os.extsep, 1)[0]
# outname = os.path.join(STUDY_PATH, "{}_v16_bvbabel.nii.gz".format(basename))
# img = nb.Nifti1Image(data, affine=np.eye(4))
# nb.save(img, outname)

print("Finished.")
