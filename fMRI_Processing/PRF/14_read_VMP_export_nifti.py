"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from scipy import ndimage


SUBJ = 'sub-01'
SESS='sess-03'
RUN='AVG'
FILE_VMR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/{}_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr".format(SUBJ, SUBJ)
FILE = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/{}/PRF_VTC_cut_2x/PRF/{}_prf_mapping_run-{}_radious5_STIMULUS.vmp".format(SUBJ, SESS, SUBJ, RUN)
# =============================================================================
#// Load VMR
header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR)
dims = np.shape(data_vmr)
print(dims)

# Load VMP
header, data = bvbabel.vmp.read_vmp(FILE)
n_map = np.shape(data)[-1]
new_data = np.zeros((dims[0], dims[1], dims[2], n_map), dtype=np.double)
print(np.shape(data))
#// See header information
pprint.pprint(header)

#// Adjusting axes according to BV convention
header["XEnd"] = int(header["XEnd"] / 2)
header["XStart"] = int(header["XStart"] / 2)

header["YEnd"] = int(header["YEnd"]/ 2)
header["YStart"] = int(header["YStart"] / 2)

header["ZEnd"] = int(header["ZEnd"] / 2)
header["ZStart"] = int(header["ZStart"] / 2)

# // Add data
mXStart = dims[0] -header["ZEnd"]-1
mXEnd = dims[0] -header["ZStart"]-1

mYStart = dims[1] -header["XEnd"]-1
mYEnd = dims[1] -header["XStart"]-1

mZStart = dims[2] -header["YEnd"]-1
mZEnd = dims[2] -header["YStart"]-1

new_data[mXStart:mXEnd, mYStart:mYEnd, mZStart:mZEnd, :] = data

# Export NIFTI
# // Zoom
zoom_data = np.zeros([dims[0], dims[1],dims[2]], dtype=np.int16)
zoom_data[new_data[..., 1] == 1] = 1
zoom_data[new_data[..., 2] == 2] = 2
zoom_data[new_data[..., 3] == 3] = 3
result = ndimage.zoom(zoom_data, 2, output=np.int16, mode='nearest', order=0, prefilter='False')

basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel_res2x_int16.nii.gz".format(basename)
img = nb.Nifti1Image(result, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
