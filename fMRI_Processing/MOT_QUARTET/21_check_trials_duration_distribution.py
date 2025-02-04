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
# SUBJ = ['sub-01']
TASK = 'amb'
# =============================================================================
mean_dur = np.zeros([len(SUBJ), 5])
std_dur = np.zeros([len(SUBJ), 5])
mean_ntr = np.zeros([len(SUBJ), 5])
for itsu, su in enumerate(SUBJ):

    # PRT data
    NII_PRT = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_PRT.nii.gz".format(su, TASK, su)

    # TRIAL duration data
    NII_DUR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_PRT_labels-durations.nii.gz".format(su, TASK, su)

    # TRIAL labels
    NII_LAB = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_PRT_labels-trials.nii.gz".format(su, TASK, su)

    OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/voxel-wise_carpet/".format(su, TASK)

    # =============================================================================
    # Output directory
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)
        print("  Output directory: {}\n".format(OUTDIR))

    # Load PRT segmentation file
    nii = nb.load(NII_PRT)
    data_prt = np.asarray(nii.dataobj)
    data_prt = np.int_(data_prt)
    labels_prt = np.unique(data_prt)
    nr_conditions = labels_prt.size
    print(f"  Nr. of conditions in PRT {nr_conditions}")

    # Load PRT TRIAL segmentation file
    nii = nb.load(NII_LAB)
    data_trials = np.asarray(nii.dataobj)
    data_trials = np.int_(data_trials)
    labels_trials = np.unique(data_trials)
    nr_tot_trials = labels_trials.size
    print(f"  Nr. of trials in PRT {nr_tot_trials}")

    # Load TRIAL DURATION segmentation file
    nii = nb.load(NII_DUR)
    data_dur = np.asarray(nii.dataobj)

    # For condition types: Horizontal --> 2; Vertical --> 3
    # Get average duration time

    for itco, cond in enumerate(labels_prt):
        print('Condition {}'.format(cond))
        print(np.shape(data_prt))
        print(np.shape(data_dur))

        idx_cond = (data_prt == cond)

        # Compute duration per condition type
        dur = data_dur[idx_cond]
        mean_dur[itsu, itco] = np.mean(dur)
        std_dur[itsu, itco] = np.std(dur)

        # Compute number of trials per condition type
        trials = data_trials[idx_cond]
        temp_trials = np.unique(trials)
        nr_trials = temp_trials.size
        mean_ntr[itsu, itco] = nr_trials

print('Mean nr_trials: [subject x condition]')
print(mean_ntr)
print('Average nr_trials across subject')
print(np.mean(mean_ntr, 0))
print('STD nr_trials across subject')
print(np.std(mean_ntr, 0))

#
# print('Mean duration: [subject x condition]')
# print(mean_dur)
# print('Average `duration` across subject')
# print(np.mean(mean_dur, 0))
# print('STD duration across subject')
# print(np.std(std_dur, 0))
