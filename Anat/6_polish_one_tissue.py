"""Polish segmentations through morphology and smoothing."""

import os
import nibabel as nb
import numpy as np
from scipy.ndimage import morphology, generate_binary_structure
from scipy.ndimage import gaussian_filter

SUBJ = 'sub-06'

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/02_AdvSeg'.format(SUBJ)

FILE = 'sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x_ETC-7x-R5_WM_bvbabel_bin_v01.nii.gz'

# Load data
nii = nb.load(os.path.join(STUDY_PATH, FILE))
data = np.asarray(nii.dataobj)

# Separate tissues
mask = data > 0

struct = generate_binary_structure(3, 1)  # 1 jump neighbourbhood

# Polish cerebrum
cereb = mask
cereb = morphology.binary_dilation(cereb, structure=struct, iterations=1)
cereb = gaussian_filter(cereb.astype(float), sigma=2)
cereb = cereb > 0.5
cereb = morphology.binary_erosion(cereb, structure=struct, iterations=1)

out = cereb

# Remove floading pieces
# cereb = mask
# cereb = morphology.binary_erosion(cereb, structure=struct, iterations=3)
#
# cereb = morphology.binary_dilation(cereb, structure=struct, iterations=20)
#
# out = cereb

# Save as nifti
basename, ext = nii.get_filename().split(os.extsep, 1)
out = nb.Nifti1Image(out.astype(int), header=nii.header, affine=nii.affine)
nb.save(out, "{}_polished.{}".format(basename, ext))

print('Finished.')
