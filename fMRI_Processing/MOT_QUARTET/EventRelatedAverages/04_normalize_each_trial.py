"""Normalize timecourse of each trial.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-09', 'sub-08', 'sub-10']
TASK = 'amb'
# =============================================================================
for su in SUBJ:
    # Trial labeled protocol
    NII_PRT ="/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}_v02/{}_VOICarpet_PRT.nii.gz".format(su, TASK, su)

    # Trial labeled protocol
    NII_PRTPERTRIAL = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}_v02/{}_VOICarpet_PRT_labels-trials.nii.gz".format(su, TASK, su)

    # Timeseries data
    NII_TC = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}_v02/{}_VOICarpet.nii.gz".format(su, TASK, su)

    OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}_v02/".format(su, TASK)

    # =============================================================================
    # Output directory
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)
        print("  Output directory: {}\n".format(OUTDIR))

    # -----------------------------------------------------------------------------
    # Load nifti time course
    nii = nb.load(NII_TC)
    data = nii.get_fdata()
    nr_timepoints = data.shape[0]
    nr_voxels = data.shape[1]
    print(f"  Nr. timepoints {nr_timepoints}")
    print(f"  Nr. voxels {nr_voxels}")

    # Load protocol of conditions per trial (prtpt)
    nii_prt = nb.load(NII_PRT)
    data_prt = np.asarray(nii_prt.dataobj)
    data_prt = np.int_(data_prt)
    labels_cond = np.unique(data_prt)[1:]
    nr_conditions = labels_cond.size
    print(f"  Nr. conditions {nr_conditions}")

    # Load protocol of uniquely labeled trials
    nii_prtpt = nb.load(NII_PRTPERTRIAL)
    data_prtpt = np.asarray(nii_prtpt.dataobj)
    data_prtpt = np.int_(data_prtpt)
    labels_trials = np.unique(data_prtpt)
    nr_trials = labels_trials.size
    print(f"  Nr. trials (all) {nr_trials}")

    nr_trials_per_cond = np.zeros(nr_conditions)
    for i, c in enumerate(labels_cond):
        temp = np.unique(data_prtpt[data_prt == c])
        nr_trials_per_cond[i] = temp.size
    print(f"  Nr. trials for conditions {labels_cond}: {nr_trials_per_cond}")

    # -----------------------------------------------------------------------------
    # Normalize each trial with its first voxel value
    for i, l in enumerate(labels_trials):
        idx = data_prtpt == l
        nr_timepoints_per_trial = np.sum(data_prtpt[:, 0] == l)
        temp = data[idx].reshape(nr_timepoints_per_trial, nr_voxels)

        # Normalize to the first data point
        temp2 = temp[0, :]
        temp3 = temp - temp2
        # Percent signal change
        # !! Substitute 0 with 1 before dividing !!
        temp2[temp2 == 0] = 1
        temp4 = temp3 / temp2 * 100

        data[idx] = temp4.reshape(nr_timepoints_per_trial*nr_voxels)

    # Save
    filename = os.path.basename(NII_TC)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, f"{basename}_normalized-t0.nii.gz")
    img = nb.Nifti1Image(data, affine=nii.affine)
    nb.save(img, outname)

print("\nFinished.")
