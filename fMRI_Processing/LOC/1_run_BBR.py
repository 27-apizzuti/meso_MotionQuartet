"""BBR in BrainVoyager"""

import os
import numpy as np
import glob

#// Set input
# FMRs = ["D:\\Motion_Quartet\\sub-01\\derivatives\\func\\sess-01\\loc01\\sub-01_task-loc_acq-2depimb2_run-01_4BBR.fmr",
# "D:\\Motion_Quartet\\sub-03\\derivatives\\func\\sess-01\\loc01\\sub-03_task-loc_acq-2depimb2_run-01_4BBR.fmr",
# "D:\\Motion_Quartet\\sub-04\\derivatives\\func\\sess-01\\loc01\\sub-04_task-loc_acq-2depimb2_run-01_4BBR.fmr",
# "D:\\Motion_Quartet\\sub-05\\derivatives\\func\\sess-01\\loc01\\sub-05_task-loc_acq-2depimb2_run-01_4BBR.fmr",
# "D:\\Motion_Quartet\\sub-06\\derivatives\\func\\sess-01\\loc01\\sub-06_task-loc_acq-2depimb2_run-01_4BBR.fmr"]
#
# VMRs = ["D:\\Motion_Quartet\\sub-01\\derivatives\\anat\\sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-03\\derivatives\\anat\\sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-04\\derivatives\\anat\\sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-05\\derivatives\\anat\\sub-05_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-06\\derivatives\\anat\\sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr"]
FMRs = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-07\\derivatives\\func\\sess-01\\loc01\\sub-07_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS.fmr"]

VMRs = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-07\\derivatives\\anat\\sub-07_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr"]

for it, fmr_file in enumerate(FMRs):
    print("Run BBR on {}".format(fmr_file))
    #// Run BBR
    doc_vmr = bv.open(VMRs[it])
    doc_vmr = bv.active_document
    doc_vmr.coregister_fmr_to_vmr_using_bbr(fmr_file)



print("Finished.")
