"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from scipy import ndimage


SUBJ = ['sub-03', 'sub-06']
SESS = 'sess-02'
HEMI = ['LH', 'RH']
RUN='AVG'
for su in SUBJ:

    FILE = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/{}/PRF_VTC_cut_2x/PRF/{}_prf_mapping_run-{}_radious5_STIMULUS_bvbabel_res2x_int16.nii.gz".format(su, SESS, su, RUN)
    for hem in HEMI:
        print('Exporting stimulus-PRF location for {} {}'.format(su, hem))
        MASK = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/05_ROI_seg/voronoi/{}_visual_areas_hMT_{}_bvbabel_rim_cortMask_voronoi_noCapsule.nii.gz".format(su, su, hem)

        # =============================================================================
        nii_file = nb.load(FILE)
        data_file = np.asarray(nii_file.dataobj)

        nii_mas = nb.load(MASK)
        data_mas = np.asarray(nii_mas.dataobj)

        #// Save new nifti
        data_file[data_mas != 2] = 0

        basename = FILE.split(os.extsep, 1)[0]
        outname = "{}_{}_V1.nii.gz".format(basename, hem)
        img = nb.Nifti1Image(data_file, affine=np.eye(4))
        nb.save(img, outname)

        print("Finished.")
