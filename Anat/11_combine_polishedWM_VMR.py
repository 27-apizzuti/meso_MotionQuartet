"""For creating GM in Brainvoyager after surfaces are reconstructed"""
#// NOTE: After the WM_GM.vmr file is created convert it back to NIFTI using 2_.py

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat'
HEMI = ['RH', 'LH']

# Load anat VMR
FILENAME = 'sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x_ETC-7x-R5.vmr'
FILE = os.path.join(STUDY_PATH, '02_AdvSeg', FILENAME)
header, data = bvbabel.vmr.read_vmr(FILE)

# Load WM seg VMR
for hem in HEMI:
    FILENAME2 = 'sub-06_WM_{}.vmr'.format(hem)
    FILE2 = os.path.join(STUDY_PATH, '03_SurfaceRecon', '{}'.format(hem), FILENAME2)
    headerseg, dataseg = bvbabel.vmr.read_vmr(FILE2)

    data[dataseg == 240] = 240

# Save VMR
outname = os.path.join(STUDY_PATH, '02_AdvSeg', 'sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x_ETC-7x-R5_WM.vmr')
bvbabel.vmr.write_vmr(outname, header, data)
print("Finished.")
