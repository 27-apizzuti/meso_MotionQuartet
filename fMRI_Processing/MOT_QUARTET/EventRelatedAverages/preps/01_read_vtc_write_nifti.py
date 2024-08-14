"""Read BrainVoyager VTC and export as NIfTI.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import bvbabel
import nibabel as nb
from pprint import pprint
from glob import glob

# =============================================================================
SUBJ = ['sub-01']
task = 'phy'
# =============================================================================
for su in SUBJ:
	# FILES = [
	# 	glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-01/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-01_*.vtc".format(su, su, task)),
	# 	glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-01/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-02_*.vtc".format(su, su, task)),
	# 	glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-01/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-03_*.vtc".format(su, su, task)),
	# 	glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-01/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-04_*.vtc".format(su, su, task)),
	# 	glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-02/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-01_*.vtc".format(su, su, task)),
	# 	glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-02/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-02_*.vtc".format(su, su, task)),
	# 	glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-02/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-03_*.vtc".format(su, su, task))]
	FILES = [
		glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/sess-02/MOT_VTC_cut_2x/{}_task-{}_acq-2depimb2_run-04_*.vtc".format(su, su, task))]

	OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-{}".format(su, task)

	# -----------------------------------------------------------------------------
	# Output directory
	if not os.path.exists(OUTDIR):
	    os.makedirs(OUTDIR)
	    print("  Output directory: {}\n".format(OUTDIR))

	# -----------------------------------------------------------------------------
	for f in FILES:
		# Load vtc
		if len(f) > 0:
			header, data = bvbabel.vtc.read_vtc(f[0], rearrange_data_axes=False)

			# See header information
			print('Converting VTC: {}'.format(f[0]))

			# Transpose axes
			data = np.transpose(data, [0, 2, 1, 3])
			# Flip axes
			data = data[::-1, ::-1, ::-1, :]

			# Export nifti
			filename = os.path.basename(f[0])
			basename, ext = filename.split(os.extsep, 1)
			outname = os.path.join(OUTDIR, f"{basename}_bvbabel.nii.gz")
			img = nb.Nifti1Image(data, affine=np.eye(4))
			nb.save(img, outname)
		else:
			print('Time course does not exist')
		print("\n")

print("\nFinished.")
