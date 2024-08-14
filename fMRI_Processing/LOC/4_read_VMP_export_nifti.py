"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-01/derivatives'

# Reference nifit
REF_NIFTI = 'sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_bvbabel.nii.gz'
nii = nb.load(os.path.join(STUDY_PATH, 'anat', REF_NIFTI))
nii_data = np.asarray(nii.dataobj)

# VMP
FILENAME = 'sub-01_loc.vmp'
FILE = os.path.join(STUDY_PATH, 'func', 'sess-01', 'loc01', 'GLM', FILENAME)
# =============================================================================
#// Create new NIFTI with the same dimensions of VMR
new_data = np.zeros(np.shape(nii_data))

# Load vmp
header, data = bvbabel.vmp.read_vmp(FILE)
#// See header information
pprint.pprint(header)

#// Adjusting axes according to BV convention
dims = np.shape(new_data)

mXStart = dims[0] -header["ZEnd"]-1
mXEnd = dims[0] -header["ZStart"]-1

mYStart = dims[1] -header["XEnd"]-1
mYEnd = dims[1] -header["XStart"]-1

mZStart = dims[2] -header["YEnd"]-1
mZEnd = dims[2] -header["YStart"]-1

new_data[mXStart:mXEnd, mYStart:mYEnd, mZStart:mZEnd] = data


# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(new_data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
