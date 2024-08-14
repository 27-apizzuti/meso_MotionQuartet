"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-03/derivatives/test-volume-to-Surface'
SUBJ = 'sub-06'

# VMR
FILENAME = 'sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC_ISO_ACPC.vmr'
FILE = os.path.join(STUDY_PATH, FILENAME)
header, data = bvbabel.vmr.read_vmr(FILE)

# Export nifti
basename = FILENAME.split(os.extsep, 1)[0]
outname = os.path.join(STUDY_PATH, "{}_bvbabel.nii.gz".format(basename))
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
