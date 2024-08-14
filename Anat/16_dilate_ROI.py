"""Polish segmentations through morphology and smoothing."""
# //NOTE: Before running this script run: fslmaths sub-03_visual_areas_hMT_LH_bvbabel_rim_voronoi.nii.gz -uthr 6 -bin sub-03_visual_areas_hMT_LH_bvbabel_rim_voronoi_noCapsule.nii.gz
import os
import nibabel as nb
import numpy as np
from scipy.ndimage import morphology, generate_binary_structure
from scipy.ndimage import gaussian_filter

SUBJ = 'sub-04'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/05_ROI_seg'.format(SUBJ)
FILE = 'sub-04_visual_areas_hMT_RH_bvbabel_rim_voronoi_bin_noCapsule.nii.gz'.format(SUBJ)

# Load data
nii = nb.load(os.path.join(STUDY_PATH, FILE))
data = np.asarray(nii.dataobj)

# Separate tissues
mask = data > 0

struct = generate_binary_structure(3, 1)  # 1 jump neighbourbhood

# Polish cerebrum1
cereb = mask

cereb = morphology.binary_dilation(cereb, structure=struct, iterations=30)
cereb = gaussian_filter(cereb.astype(float), sigma=0.5)
cereb = cereb > 0.75

out = cereb

# Save as nifti
basename, ext = nii.get_filename().split(os.extsep, 1)
out = nb.Nifti1Image(out.astype(int), header=nii.header, affine=nii.affine)
nb.save(out, "{}_dilated.{}".format(basename, ext))

print('Finished.')
