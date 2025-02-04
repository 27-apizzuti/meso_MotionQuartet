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
TASK = 'phy'
# =============================================================================
tsnr_roi = np.zeros([len(SUBJ), 4])

for itsu, su in enumerate(SUBJ):

    # Timeseries data
    NII_TC = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/voxel-wise_carpet/{}_VOICarpet.nii.gz".format(su, TASK, su)

    # ROI labels
    NII_ROI = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/voxel-wise_carpet/{}_VOICarpet_labels-vois.nii.gz".format(su, TASK, su)

    # Run labels
    NII_RUN = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/voxel-wise_carpet/{}_VOICarpet_labels-runs.nii.gz".format(su, TASK, su)

    OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/voxel-wise_carpet/".format(su, TASK)

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

    # Load ROI segmentation file
    nii = nb.load(NII_ROI)
    data_roi = np.asarray(nii.dataobj)
    data_roi = np.int_(data_roi)
    labels_roi = np.unique(data_roi)
    nr_roi = labels_roi.size
    print(f"  Nr. regions of interest {nr_roi}")

    # Load RUN segmentation file
    nii = nb.load(NII_RUN)
    data_run = np.asarray(nii.dataobj)
    data_run = np.int_(data_run)
    labels_run = np.unique(data_run)
    nr_runs = labels_run.size
    print(f"  Nr. runs {nr_runs}")

    # For each run, compute voxe-wise tSNR as mean / std
    tsnr = np.zeros([nr_voxels, nr_runs])
    for itvox in range(0, nr_voxels-1):

        for irun, run in enumerate(labels_run):
            ts = data[:, itvox]
            data_temp = data_run[:, itvox]
            roi_temp = data_roi[:, itvox]

            idx_run = data_temp == run
            ts_vox = ts[idx_run]

            # Compute tSNR
            ts_mean = np.mean(ts_vox)
            ts_std = np.std(ts_vox)
            tsnr[itvox, irun] = ts_mean / ts_std

    print(np.shape(tsnr))
    # Average tSNR across RUNS
    tsnr_avgruns = np.nanmean(tsnr, 1)

    print(np.shape(tsnr_avgruns))

    # Average tSNR across voxels within the same ROI
    data_roi_vox = np.transpose(data_roi[0, :])
    print(np.shape(data_roi_vox))

    for itroi, roi in enumerate(labels_roi):
        idx_roi = data_roi_vox == roi

        tsnr_roi[itsu, itroi] = np.nanmean(tsnr_avgruns[idx_roi])

print('Computing tSNR: [subject x rois]')
print(tsnr_roi)
print('Average tSNR across subject')
print(np.mean(tsnr_roi, 0))
print('STD tSNR across subject')
print(np.std(tsnr_roi, 0))




    # nr_trials_per_cond = np.zeros(nr_conditions)
    # for i, c in enumerate(labels_cond):
    #     temp = np.unique(data_prtpt[data_prt == c])
    #     nr_trials_per_cond[i] = temp.size
    # print(f"  Nr. trials for conditions {labels_cond}: {nr_trials_per_cond}")
    #
    # # -----------------------------------------------------------------------------
    # # Normalize each trial with its first voxel value
    # for i, l in enumerate(labels_trials):
    #     idx = data_prtpt == l
    #     nr_timepoints_per_trial = np.sum(data_prtpt[:, 0] == l)
    #     temp = data[idx].reshape(nr_timepoints_per_trial, nr_voxels)
    #
    #     # Normalize to the first data point
    #     temp2 = temp[0, :]
    #     temp3 = temp - temp2
    #     # Percent signal change
    #     # !! Substitute 0 with 1 before dividing !!
    #     temp2[temp2 == 0] = 1
    #     temp4 = temp3 / temp2 * 100
    #
    #     data[idx] = temp4.reshape(nr_timepoints_per_trial*nr_voxels)
    #
    # # Save
    # filename = os.path.basename(NII_TC)
    # basename, ext = filename.split(os.extsep, 1)
    # outname = os.path.join(OUTDIR, f"{basename}_normalized-t0.nii.gz")
    # img = nb.Nifti1Image(data, affine=nii.affine)
    # nb.save(img, outname)

print("\nFinished.")
