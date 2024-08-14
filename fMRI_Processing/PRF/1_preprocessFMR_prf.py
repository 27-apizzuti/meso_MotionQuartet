# preprocess FMR: slictime, moco, highpass ; AP
# This script was used to preprocess high-res and lo-res functional data acquired with CMRR sequence;

import numpy as np
import os
import glob

print("Hello.")

# =============================================================================
STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ["sub-09","sub-10"]
SESS = [2]
TASK = ["prf"]

# Parameters
# HPF_CUTOFF = 3
for su in SUBJ:
    PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives', 'func')

    for se in SESS:
        path_in = os.path.join(PATH_FMR, 'sess-0{}'.format(se))
        for tas in TASK:
            runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
            # MOCO_REF_VOL = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'sess-0{}'.format(se), 'phy01', '{}_task-phy_acq-2depimb2_run-01.fmr'.format(su))
            MOCO_REF_VOL = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'sess-0{}'.format(se), 'prf01', '{}_task-prf_acq-2depimb2_run-01.fmr'.format(su))

            for path_run in runs:
                print(path_run)
                docPathIn = glob.glob(os.path.join(path_run, '*.fmr'))[0]
                #1// Correct Slice Timing
                docFMR = bv.open(docPathIn)
                docFMR.correct_slicetiming_using_timingtable(2) # window. sinc interpolation
                Fnme_newFMR = docFMR.preprocessed_fmr_name
                docFMR.close()

                #2// Motion Correction
                docFMR=bv.open(Fnme_newFMR)
                docFMR.correct_motion_to_run_ext(MOCO_REF_VOL, 1, 2, 1, 100, 1, 1)
                Fnme_newFMR = docFMR.preprocessed_fmr_name
                docFMR.close()

                # #3 // High-pass filtering
                # docFMR=bv.open(Fnme_newFMR)
                # docFMR.filter_temporal_highpass_glm_fourier(HPF_CUTOFF)
                # docFMR.close()
