# create mosaic FMR ; Starting from standard .dcm organization folder
# Run in BrainVoyager

import numpy as np
import os
import math
import glob

print("Create FMR files.")

# =============================================================================
STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ["sub-01", "sub-03", "sub-04", "sub-05","sub-06","sub-07","sub-08", "sub-09", "sub-10"]
SESS = ["sess-03"]
# =============================================================================

for su in SUBJ:
    for se in SESS:
        print('Working on {}'.format(su))
        PATH_DCM = os.path.join(STUDY_PATH, su, 'sourcedata', se, 'DICOM')
        PATH_FMR = os.path.join(STUDY_PATH, su, 'derivatives')

        option_file = "5_options_bids_fmr.txt"

        # Create output tree folders
        if not os.path.exists(PATH_FMR):
            os.mkdir(PATH_FMR)
        PATH_FMR = os.path.join(PATH_FMR, 'func')
        if not os.path.exists(PATH_FMR):
            os.mkdir(PATH_FMR)
        PATH_FMR = os.path.join(PATH_FMR, se)
        if not os.path.exists(PATH_FMR):
            os.mkdir(PATH_FMR)

        # =============================================================================

        # Reading Information from .txt file
        info = np.loadtxt(os.path.join(STUDY_PATH, su, 'sourcedata', se, option_file), dtype=str, delimiter='\t')
        series = info[1:, 0]
        task = info[1:, 1]
        acq = info[1:, 2]
        n_run = info[1:, 3]
        fld = info[1:, 4]   # destination folder (func or anat)
        vols = info[1:, 5]
        slices = info[1:, 6]
        x_dim = info[1:, 7]
        y_dim = info[1:, 8]

        if not os.path.exists(PATH_FMR):
            os.mkdir(PATH_FMR)

        for ri in range(len(series)):
            # pathIn = os.path.join(PATH_DCM, str(series[ri]), seq_prefix + str(series[ri]) +'-0001-00001.dcm')
            pathIn = glob.glob(os.path.join(PATH_DCM, str(series[ri]), '*1.dcm'))[0]
            print(pathIn)
            pathOut = os.path.join(PATH_FMR, str(task[ri]) + str(n_run[ri]))
            bids_name = su + "_task-" + str(task[ri]) + "_acq-" + str(acq[ri]) + "_run-" + str(n_run[ri])
            if not os.path.exists(pathOut):
                os.mkdir(pathOut)
            print(math.sqrt(int(slices[ri])))

            mosaic_size_row = int(math.ceil(math.sqrt(int(slices[ri])))) * int(x_dim[ri])
            mosaic_size_col = int(math.ceil(math.sqrt(int(slices[ri])))) * int(y_dim[ri])
            print(math.ceil(math.sqrt(int(slices[ri]))))
            print(mosaic_size_col)

            docFMR = brainvoyager.create_mosaic_fmr(pathIn, int(vols[ri]), 0, 0, int(slices[ri]), bids_name, 0, int(mosaic_size_row), int(mosaic_size_col), int(x_dim[ri]), int(y_dim[ri]), 2, pathOut)
