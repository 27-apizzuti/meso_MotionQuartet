"""Read BrainVoyager vmr and export nifti.
NOTE: First export --> improve brain extraction """


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = 'sub-06'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/'.format(SUBJ)

# # Load nifti
# FILENAME = os.path.join(STUDY_PATH, '02_AvdSeg', '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_mask_ETC-7x-R5_bvbabel.nii.gz'.format(SUBJ))
# nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
# nii_data = np.asarray(nii.dataobj)
#
# # Load mask
# MASK = os.path.join(STUDY_PATH, '02_AvdSeg', '{}_WM-v01_CC.nii.gz'.format(SUBJ))
# ma =  nb.load(os.path.join(STUDY_PATH, MASK))
# ma_data = np.asarray(ma.dataobj)
# nii_data[ma_data == 1] = 240
#
# # Save nifti
# outname = os.path.join(STUDY_PATH, '02_AvdSeg', '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_mask_ETC-7x-R5_WM_polished.nii.gz'.format(SUBJ))
# img = nb.Nifti1Image(nii_data, affine=np.eye(4))
# nb.save(img, outname)
#


# Load nifti
FILENAME = os.path.join(STUDY_PATH, '02_AdvSeg', 'sub-06_RH_WM.nii.gz'.format(SUBJ))
nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
nii_data = np.asarray(nii.dataobj)
nii_data[nii_data == 1] = 240


REF_VMR = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'.format(SUBJ))
header, data = bvbabel.vmr.read_vmr(REF_VMR)
print('Converting NIFTI to VMR')

outname = os.path.join(STUDY_PATH, '03_SurfaceRecon', '{}_WM_RH.vmr'.format(SUBJ))
bvbabel.vmr.write_vmr(outname, header, nii_data)
