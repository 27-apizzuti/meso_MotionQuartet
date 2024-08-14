"""For creating GM in Brainvoyager after surfaces are reconstructed"""
#// NOTE: After the WM_GM.vmr file is created convert it back to NIFTI using 2_.py

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

# Load anat VMR
FILENAME = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-04/derivatives/anat/sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x.vmr"
header, data = bvbabel.vmr.read_vmr(FILENAME)
new_data = np.zeros(np.shape(data))

print(np.shape(new_data))
# Brainmask
FILE2 = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-04/derivatives/anat/02_AdvSeg/sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel_SS_BFC_STEDI_n10_s0pt5_r2pt0_g1_mask_ETC-7x-R5_WM_GM.vmr"
header2, data2 = bvbabel.vmr.read_vmr(FILE2)

idx = data2 > 0
print(np.shape(idx))

# Polished data
new_data[idx] = data[idx]


# Save VMR
outname = os.path.join('/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-04/derivatives/anat/sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_polished.vmr')
bvbabel.vmr.write_vmr(outname, header, new_data)
print("Finished.")
