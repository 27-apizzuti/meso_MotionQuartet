"""Turn PRT files into labels for fMRI carpet timeseries.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from glob import glob
# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-09', 'sub-08', 'sub-10']
TR_in_ms = 2000
TASK = 'amb'

# This affine gives starting indices at lower left hand corner in ITKSNAP
CUSTOM_AFFINE = np.array([[-1, 0, 0, 0],
		    			  [ 0, 1, 0, 0],
						  [ 0, 0, 1, 0],
				   		  [ 0, 0, 0, 1]])

# =============================================================================
for su in SUBJ:
	
	# BrainVoyager stimulation protocol files
	PRTS = []
	
	if TASK == 'amb':
		PRTS_FILES = [sorted(glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/Protocols/sess-01/Exp1_Amb_MotQuart/Protocols/Protocol_{}_Protocols_sess-01_*.prt".format(su, su))), 
    	sorted(glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/Protocols/sess-02/Exp1_Amb_MotQuart/Protocols/Protocol_{}_Protocols_sess-02_*.prt".format(su, su)))]
	else:
		PRTS_FILES = [sorted(glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/Protocols/sess-01/Exp1_Phys_MotQuart/Protocols/Protocol_Exp1_Phys_MotQuart_run-*.prt".format(su))), 
    	sorted(glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/Protocols/sess-02/Exp1_Phys_MotQuart/Protocols/Protocol_Exp1_Phys_MotQuart_run-*.prt".format(su)))]

	for it in PRTS_FILES:
		for t in it:
			PRTS.append(t)

	# Reference carpet timecourse
	NII_TC = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}_v02/{}_VOICarpet.nii.gz".format(su, TASK, su)

	OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}_v02".format(su, TASK)
	OUTBASENAME = "{}".format(su)

	# -----------------------------------------------------------------------------
	# Output directory
	if not os.path.exists(OUTDIR):
	    os.makedirs(OUTDIR)
	    print("  Output directory: {}\n".format(OUTDIR))

	# -----------------------------------------------------------------------------
	# Determine necessary information
	# -----------------------------------------------------------------------------
	nr_runs = len(PRTS)
	print(f"  Nr. runs {nr_runs}")

	nii1 = nb.load(NII_TC)
	data1 = np.asarray(nii1.dataobj)

	nr_timepoints = data1.shape[0] // nr_runs
	nr_voxels = data1.shape[1]
	print(f"  Nr. timepoints {nr_timepoints}")
	print(f"  Nr. voxels {nr_voxels}")


	carpet_prt = np.zeros((nr_timepoints, nr_voxels, nr_runs))

	# -----------------------------------------------------------------------------
	# Read PRT and put it into 2D nifti format
	# -----------------------------------------------------------------------------
	for n in range(nr_runs):
		header_prt, data_prt = bvbabel.prt.read_prt(PRTS[n])

		# Print header information
		print("\nPRT header")
		for key, value in header_prt.items():
		    print("  ", key, ":", value)

		# Print data
		print("\nPRT data")
		for d in data_prt:
		    for key, value in d.items():
		        print("  ", key, ":", value)
		    print("")

		# Convert PRT to nifti
		if TASK == 'amb':
			for i in range(int(header_prt["NrOfConditions"])):
				for ii in range(int(data_prt[i]["NrOfOccurances"])):
					j = round(float(data_prt[i]["Time start"][ii]) / TR_in_ms);
					k = round(float(data_prt[i]["Time stop"][ii]) / TR_in_ms);
					carpet_prt[j:k, :, n] = i
		else:
			for i in range(int(header_prt["NrOfConditions"])):
				for ii in range(int(data_prt[i]["NrOfOccurances"])):
					j = data_prt[i]["Time start"][ii]-1;
					k = data_prt[i]["Time stop"][ii];
					carpet_prt[j:k, :, n] = i		

	# Unravel
	carpet_prt = carpet_prt.transpose([2, 0, 1])
	carpet_prt = carpet_prt.reshape([nr_runs*nr_timepoints, nr_voxels])

	# Save
	outname = os.path.join(OUTDIR, f"{OUTBASENAME}_VOICarpet_PRT.nii.gz")
	img = nb.Nifti1Image(carpet_prt, affine=CUSTOM_AFFINE)
	nb.save(img, outname)

print("\nFinished.")
