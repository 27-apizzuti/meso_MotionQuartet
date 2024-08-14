"""Read BrainVoyager vmr and export nifti."""


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-07", "sub-08", "sub-09", "sub-10"]
SES = [1]

for su in SUBJ:
    print('Converting VMR anatomy for {}'.format(su))
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat')
    # VMR
    FILENAME = '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr'.format(su)
    FILE = os.path.join(PATH_IN, FILENAME)
    header, data = bvbabel.vmr.read_vmr(FILE)

    # Export nifti
    basename = FILENAME.split(os.extsep, 1)[0]
    outname = os.path.join(PATH_IN, "{}_bvbabel.nii.gz".format(basename))
    img = nb.Nifti1Image(data, affine=np.eye(4))
    nb.save(img, outname)

    # V16
    FILENAME = '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.v16'.format(su)
    FILE = os.path.join(PATH_IN, FILENAME)
    header, data = bvbabel.v16.read_v16(FILE)

    # Export nifti
    basename = FILENAME.split(os.extsep, 1)[0]
    outname = os.path.join(PATH_IN, "{}_v16_bvbabel.nii.gz".format(basename))
    img = nb.Nifti1Image(data, affine=np.eye(4))
    nb.save(img, outname)

print("Finished.")
