"""Turn nifti timeseries with ROIs into carpet timeseries.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb
from glob import glob

# =============================================================================
SUBJ = SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-09', 'sub-08', 'sub-10']

TASK = 'amb'

# This affine gives starting indices at lower left hand corner in ITKSNAP
CUSTOM_AFFINE = np.array([[-1, 0, 0, 0],
		    			  [ 0, 1, 0, 0],
						  [ 0, 0, 1, 0],
				   		  [ 0, 0, 0, 1]])
# =============================================================================
for su in SUBJ:
	# Timecourses
	NII_TC = sorted(glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/{}_task-{}_acq-2depimb2_*res2x_bvbabel.nii.gz".format(su, TASK, su, TASK)))
	# print(NII_TC)

	# Voxels of interest / regions of interest
	NII_VOI = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}/{}_combined_4ROIs_VOIinVTCspace.nii.gz".format(su, TASK, su)


	OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}_v02".format(su, TASK)
	OUTBASENAME = "{}".format(su)

	# -----------------------------------------------------------------------------
	# Output directory
	if not os.path.exists(OUTDIR):
	    os.makedirs(OUTDIR)
	    print("  Output directory: {}\n".format(OUTDIR))

	# -----------------------------------------------------------------------------
	# Figure out the necessary information
	# -----------------------------------------------------------------------------
	nr_runs = len(NII_TC)
	print(f"  Nr. runs {nr_runs}")

	# Load nifti time course
	nii_temp = nb.load(NII_TC[0])
	data_temp = np.asarray(nii_temp.dataobj)
	nr_timepoints = data_temp.shape[-1]
	print(f"  Nr. timepoints (per run) {nr_timepoints}")

	# Load nifti voxels on interest
	nii_voi = nb.load(NII_VOI)
	data_voi = np.asarray(nii_voi.dataobj)

	# Determine labels of ROI's
	labels = np.unique(data_voi)[1:]
	labels = labels.astype(int)
	nr_labels = labels.size
	print(f"  Nr. labels {nr_labels}")

	# -----------------------------------------------------------------------------
	# Fill in the carpet by looping over runs
	# -----------------------------------------------------------------------------
	carpet = np.zeros((nr_timepoints, nr_labels, nr_runs))
	carpet_vois = np.zeros((nr_timepoints, nr_labels, nr_runs ))
	carpet_runs = np.zeros((nr_timepoints, nr_labels, nr_runs))

	for n in range(nr_runs):
	
		if n > 0:  # First timeseries is already loaded before the loop
			nii_temp = nb.load(NII_TC[n])
			data_temp = np.asarray(nii_temp.dataobj)

		# Step 5: Pull out time courses
		for i in labels:
			# Pull out ROI data
			idx_roi = data_voi == i
			temp = np.mean(data_temp[idx_roi], axis=0)
			print(data_temp[idx_roi].shape)
			print(temp.shape)

			# Insert to carpet			
			carpet[:, i-1, n] = temp
			carpet_vois[:, i-1, n] = i
			carpet_runs[:, i-1, n] = n+1

		print(f"  {n+1}/{nr_runs}")

	# -----------------------------------------------------------------------------
	# Unravel carpets
	# -----------------------------------------------------------------------------
	carpet = carpet.transpose([2, 0, 1])
	carpet_vois = carpet_vois.transpose([2, 0, 1])
	carpet_runs = carpet_runs.transpose([2, 0, 1])

	carpet = carpet.reshape([nr_runs*nr_timepoints, nr_labels])
	carpet_vois = carpet_vois.reshape([nr_runs*nr_timepoints, nr_labels])
	carpet_runs = carpet_runs.reshape([nr_runs*nr_timepoints, nr_labels])

	# Save
	# -----------------------------------------------------------------------------
	outname = os.path.join(OUTDIR, f"{OUTBASENAME}_VOICarpet.nii.gz")
	img = nb.Nifti1Image(carpet, affine=CUSTOM_AFFINE)
	nb.save(img, outname)
	outname = os.path.join(OUTDIR, f"{OUTBASENAME}_VOICarpet_labels-vois.nii.gz")
	img = nb.Nifti1Image(carpet_vois, affine=CUSTOM_AFFINE)
	nb.save(img, outname)
	outname = os.path.join(OUTDIR, f"{OUTBASENAME}_VOICarpet_labels-runs.nii.gz")
	img = nb.Nifti1Image(carpet_runs, affine=CUSTOM_AFFINE)
	nb.save(img, outname)

print("\nFinished.")
