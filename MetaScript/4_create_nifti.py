"""
For a study that follows BIDS specification

    Rename Nifti files (e.g. High-res functional data SS-SI VASO or anat data)

    Input: nifti folder
    Output: nifti/func or anat

18-04-21

# Run for P01, P02, P03 (pilot)
# Run for P01, P02, P03 (sess1, sess2, sess3), P04(sess1, sess2), P05(sess1, sess2), P06(sess1, sess2, sess3)
"""

import os
import pandas as pd
import subprocess

print("Hello!")

# =============================================================================
# NIFTI input path (already created)
STUDY_PATH = "/mnt/g/Motion_Quartet"
SUBJ = ["sub-09"]
SESS = 'sess-03'
for su in SUBJ:
    PATH_NII = os.path.join(STUDY_PATH, su, 'derivatives', 'anat')
    PATH_DCM = os.path.join(STUDY_PATH, su, 'sourcedata', SESS, 'DICOM')
    option_file = '4_options_bids_nifti.txt'
    # =============================================================================
    if not os.path.exists(PATH_NII):
        os.mkdir(PATH_NII)

    # Reading Information from .txt file
    info = pd.read_csv(os.path.join(STUDY_PATH, su, 'sourcedata', SESS, option_file), sep='\t', header=None)
    series = list(info.loc[1:, 0])
    task = list(info.loc[1:, 1])
    acq = list(info.loc[1:, 2])
    n_run = list(info.loc[1:, 3])
    fld = list(info.loc[1:, 4])  # destination folder (func or anat)

    # // DICOM to NIFTI conversion
    # Execution
    for i in range(len(series)):
        path_inputDCM = os.fspath(os.path.join(PATH_DCM, series[i]))
        print("Converting series {}" .format(str(series[i])))
        # subprocess.run(["dcm2niix", "-o", PATH_NII, "-z", "y", path_inputDCM])

    # // Rename NIFTI
    print("Renaming NIFTI.")
    f_content = os.listdir(PATH_NII)
    for i in range(len(f_content)):

        basename, extension = os.path.splitext(f_content[i])
        b = basename.split('_')

        if b[0] in series:
            print("Renaming series {}" .format(str(b[0])))
            k = series.index(b[0])
            if extension == '.gz':
                bids_name = su + "_" + str(SESS) + "_acq-" + str(acq[k]) + "_" + str(n_run[k]) + ".nii" + extension
            else:
                bids_name = su + "_" + str(SESS) + "_acq-" + str(acq[k]) + "_" + str(n_run[k]) + extension

            path_old = os.fspath(os.path.join(PATH_NII, f_content[i]))
            path_new = os.fspath(os.path.join(PATH_NII, bids_name))
            print(path_old)
            os.rename(path_old, path_new)

print("Success.")
