"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

SUBJ = 'sub-04'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/'.format(SUBJ)

#// LOAD VMR
REF_VMR = os.path.join(STUDY_PATH, '{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr'.format(SUBJ))
header, data = bvbabel.vmr.read_vmr(REF_VMR)

#// lOAD VOI
VOI = os.path.join(STUDY_PATH, '04_CorticalMask', 'sub-04_RH_visual_areas_hMT.voi'.format(SUBJ))

voi_header, data_voi = bvbabel.voi.read_voi(VOI)
pprint(voi_header)
print(np.shape(data_voi[0]["Coordinates"]))
nmap = voi_header['NrOfVOIs']

# New data
new_data = np.zeros(np.shape(data))
for it in range(0, nmap):
    idx = data_voi[it]["Coordinates"]
    x = idx[:, 0]
    y = idx[:, 1]
    z = idx[:, 2]

    new_data[z, x, y] = it + 1  # +1 to skip zero

new_data = new_data[::-1,::-1, ::-1]
basename = VOI.split(os.extsep, 1)[0]
outname = os.path.join(STUDY_PATH, '{}_bvbabel.nii.gz'.format(basename))
img = nb.Nifti1Image(new_data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
