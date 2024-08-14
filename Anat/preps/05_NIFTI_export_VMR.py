"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = 'sub-06'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat'.format(SUBJ)

#// Reference VMR
REF_VMR = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr'.format(SUBJ))
header, data = bvbabel.vmr.read_vmr(REF_VMR)
print('Converting NIFTI to VMR')

# Load nifti to convert
FILENAME = '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC.nii.gz'.format(SUBJ)
nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
datanii = np.asarray(nii.dataobj)

# Save new vmr
outname = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC.vmr'.format(SUBJ))
bvbabel.vmr.write_vmr(outname, header, datanii)
