"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from scipy import ndimage
from glob import glob

SUBJ = ['sub-03', 'sub-06']
SESS = 'sess-02'
HEMI = ['LH', 'RH']
RUN='AVG'
for su in SUBJ:

    for hem in HEMI:
        FILE = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/{}/PRF_VTC_cut_2x/PRF/{}_prf_mapping_run-{}_radious5_STIMULUS_bvbabel_res2x_int16_{}_V1.nii.gz".format(su, SESS, su, RUN, hem)

        print('Checking multilaterate coverage for {} {}'.format(su, hem))

        MASK_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers".format(su)
        os.chdir(MASK_PATH)
        myfile = glob('*{}*perimeter_chunk.nii*'.format(hem))[0]
        print(myfile)
        # =============================================================================
        nii_file = nb.load(FILE)
        data_file = np.asarray(nii_file.dataobj)

        nii_mas = nb.load(os.path.join(MASK_PATH, myfile))
        data_mas = np.asarray(nii_mas.dataobj)

        #// Save new nifti
        idx = (data_mas > 0)*(data_file > 0)
        print('Coverage: {}/{}'.format(np.sum(np.sum(idx)), np.sum(np.sum(data_file > 0))))

        print("Finished.")
