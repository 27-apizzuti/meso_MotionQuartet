"""Change header with dcm2nii -> FMR. After this script, load new FMR and check slice thickness. Change from 1 to 1.8. Save it."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import glob
import matplotlib.pyplot as plt
from pprint import pprint
# =============================================================================
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-09"]
SESS = [1]
TASK = ["loc01"]

for su in SUBJ:
    PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')
    for se in SESS:
        path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se), 'loc01')
        if su == 'sub-09':
            # Load reference FMR (dicom -> nifti -> open nifti in BV)
            FMR = glob.glob(os.path.join(PATH_FMR, 'sess-02', 'prf01', 'topup_prf', '{}_task-prf_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_THPGLMF3c.fmr'.format(su)))[0]
            FMR2 = glob.glob(os.path.join(path_in, '*run-01_SCSTBL_3DMCTS_bvbabel_warped_THPGLMF3c.fmr'))[0]
            filename = os.path.join(path_in, '{}_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_warped_THPGLMF3c_fix.fmr'.format(su))
        else:
            # Load reference FMR (dicom -> nifti -> open nifti in BV)
            FMR = glob.glob(os.path.join(path_in, '{}_sess-01_task-loc_acq-2depimb3_run-01.fmr'.format(su)))[0]
            FMR2 = glob.glob(os.path.join(path_in, '*run-01_SCSTBL_3DMCTS_THPGLMF3c.fmr'))[0]
            filename = os.path.join(path_in, '{}_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_THPGLMF3c_fix.fmr'.format(su))

        header, datafmr = bvbabel.fmr.read_fmr(FMR)

        # Load FMR to correct

        header2, datafmr2 = bvbabel.fmr.read_fmr(FMR2)
        print(np.shape(datafmr))
        print(np.shape(datafmr2))
        # pprint(header)
        # print('####################')
        # pprint(header2)
        datafmr2 = datafmr2[:,::-1,:,:]
        # # Save FMR with different header
        bvbabel.fmr.write_fmr(filename, header, datafmr2)



print("Finished.")
