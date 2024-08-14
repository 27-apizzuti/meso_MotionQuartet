"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-03/derivatives/test-volume-to-Surface'
SUBJ = 'sub-06'

REF_VMR = os.path.join(STUDY_PATH, 'sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr')

#// Parte 2: Put back nifti into VMR
# Load nifti
FILENAME = 'sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel.nii.gz'
nii =  nb.load(os.path.join(STUDY_PATH, FILENAME))
data = np.asarray(nii.dataobj)
print(np.shape(data))

# # Load vmr
header, datavmr = bvbabel.vmr.read_vmr(REF_VMR)

outname = os.path.join(STUDY_PATH, 'sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_back.vmr')
bvbabel.vmr.write_vmr(outname, header, data)
