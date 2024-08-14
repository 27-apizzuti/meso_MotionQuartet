"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from copy import copy

SUBJ = 'sub-07'
STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/'.format(SUBJ)

#// LOAD VMR
REF_VMR = os.path.join(STUDY_PATH, 'sub-07_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr'.format(SUBJ))
header, data = bvbabel.vmr.read_vmr(REF_VMR)

#// LOAD NIFTI
FILENAME = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/Results/VoxelSelection/sub-07/sub-07_visual_areas_hMT_LH_bvbabel_rim_voronoi_noCapsule.nii.gz'
nii =  nb.load(FILENAME)
datanii = np.asarray(nii.dataobj)

#// lOAD VOI (as reference for the header.)
VOI = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/Results/VoxelSelection/sub-07/LH_visualareas_hMT_capsule.voi'
voi_header, data_voi = bvbabel.voi.read_voi(VOI)
nmap = voi_header['NrOfVOIs']

#// Change datanii array to match VOI
new_data = np.zeros(np.shape(datanii))
new_data = copy(datanii)
new_data = new_data[::-1,::-1, ::-1]
new_data = np.transpose(new_data, (1, 2, 0))

for it in range(0, nmap):
    # Loop over each ROI (different number and put it back)
    idx_voxels = np.argwhere(new_data == it+1)
    print(data_voi[it])
    data_voi[it]["NrOfVoxels"] = idx_voxels.shape[0]
    data_voi[it]["Coordinates"] = idx_voxels
#
outname = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/Results/VoxelSelection/sub-07/sub-07_visual_areas_hMT_LH_bvbabel_rim_voronoi_noCapsule.voi'
bvbabel.voi.write_voi(outname, voi_header, data_voi)
#
print("Finished.")
