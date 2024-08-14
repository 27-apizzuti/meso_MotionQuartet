"""Compute event related averages for each ROI.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb

# =============================================================================
SUBJ = SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-09', 'sub-08', 'sub-10']
DUR_MIN = 5
DUR_MAX = 100
TASK = 'amb'
CONDITION = [2, 3]
CONDITION_LABELS = ['Horizontal', 'Vertical']
# =============================================================================
for su in SUBJ:
    # Normalized Time course
    NII_TC = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_normalized-t0.nii.gz".format(su, TASK, su)

    # Regions of interest
    NII_ROI = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_labels-vois.nii.gz".format(su, TASK, su)

    # Conditions
    NII_CON = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_PRT.nii.gz".format(su, TASK, su)

    # Durations
    NII_DUR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_PRT_labels-durations.nii.gz".format(su, TASK, su)

    # Trials
    NII_TRI = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/{}_VOICarpet_PRT_labels-trials.nii.gz".format(su, TASK, su)

    # Output directory
    OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/ROI-wise_carpet/".format(su, TASK)

    # Output directory
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)
        print("  Output directory: {}\n".format(OUTDIR))

    # -----------------------------------------------------------------------------
    # Load nifti time course
    nii_tc = nb.load(NII_TC)
    data = nii_tc.get_fdata()
    nr_timepoints = data.shape[0]
    nr_voxels = data.shape[1]
    print(f"  Nr. timepoints : {nr_timepoints}")
    print(f"  Nr. voxels     : {nr_voxels}")

    # Load ROIs
    nii_roi = nb.load(NII_ROI)
    data_roi = np.asarray(nii_roi.dataobj)
    data_roi = data_roi.astype(np.int32)
    labels_roi = np.unique(data_roi)
    nr_rois = labels_roi.size
    print(f"  Nr. rois       : {nr_rois}")

    # Load conditions
    nii_con = nb.load(NII_CON)
    data_con = np.asarray(nii_con.dataobj)
    data_con = data_con.astype(np.int32)
    labels_con = np.unique(data_con)[1:]  # Skip 0
    nr_cons = labels_con.size
    print(f"  Nr. conditions : {nr_cons}")

    # Load durations
    nii_dur = nb.load(NII_DUR)
    data_dur = np.asarray(nii_dur.dataobj)
    data_dur = data_dur.astype(np.int32)

    # Load trials
    nii_tri = nb.load(NII_TRI)
    data_tri = np.asarray(nii_tri.dataobj)
    data_tri = data_tri.astype(np.int32)

    # -----------------------------------------------------------------------------
    # Threshold based on user parameters
    if TASK == 'amb':
        data_dur[data_dur < DUR_MIN] = 0
        data_dur[data_dur > DUR_MAX] = 0

    for co in CONDITION:
        print('Considering condition {}'.format(co))
        idx1 = data_con == co
        idx2 = data_dur != 0
        nr_trials_chosen = np.unique(data_tri[idx1 * idx2]).size
        print("Nr of chosen trials: {}/{}".format(nr_trials_chosen, np.unique(data_tri[idx1]).size))

        era_values = np.zeros([DUR_MAX, nr_rois])
        era_counts = np.zeros([DUR_MAX, nr_rois])


        for j in range(nr_rois):
            print(f"  Computing ROI: {labels_roi[j]}")
            idx0 = data_roi == labels_roi[j]
            idx3 = idx0 * idx1 * idx2

            nr_vox_roi = np.sum(idx0)//nr_timepoints
            # print(nr_vox_roi)

            label_temp_trials = np.unique(data_tri[idx3])
            print('Trials chosen for condition {}: {}'.format(co, label_temp_trials))

            for n, i in enumerate(label_temp_trials):
                idx4 = data_tri == i
                idx5 = idx3 * idx4
                dur = data_dur[idx5][0]
                temp = data[idx5]
                # print(temp.shape)
                
                # temp = np.reshape(temp, [dur, nr_vox_roi])
                # print(temp.shape)
                # print(era_values[0:dur, j-1].shape)
                era_values[0:dur, j] += temp
                era_counts[0:dur, j] += 1

        era_mean = era_values / era_counts
        
        # -----------------------------------------------------------------------------
        # Save
        filename = os.path.basename(NII_TC)
        basename, ext = filename.split(os.extsep, 1)

        outname = os.path.join(OUTDIR, f"{basename}_ERAperROI_dur_{DUR_MIN}_{DUR_MAX}_cond-{co}_sum.nii.gz")
        img = nb.Nifti1Image(era_values, affine=nii_tc.affine)
        nb.save(img, outname)

        outname = os.path.join(OUTDIR, f"{basename}_ERAperROI_dur_{DUR_MIN}_{DUR_MAX}_cond-{co}_counts.nii.gz")
        img = nb.Nifti1Image(era_counts, affine=nii_tc.affine)
        nb.save(img, outname)

        outname = os.path.join(OUTDIR, f"{basename}_ERAperROI_dur_{DUR_MIN}_{DUR_MAX}_cond-{co}_mean.nii.gz")
        img = nb.Nifti1Image(era_mean, affine=nii_tc.affine)
        nb.save(img, outname)

print("\nFinished.")
