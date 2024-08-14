"""BBR in BrainVoyager"""
#// This is done with GUI since we need to activate the grid option

import os
import numpy as np
import glob

#// Set input
# FMRs = ["D:\\Motion_Quartet\\sub-01\\derivatives\\func\\sess-03\\topup_prf\\bbr\\sub-01_prf_AP_undist_2vols",
# "D:\Motion_Quartet\sub-03\derivatives\func\sess-02\topup_prf\bbr\sub-03_prf_AP_undist_2vols",
# "D:\Motion_Quartet\sub-04\derivatives\func\sess-04\topup_prf\bbr\sub-04_prf_AP_undist_2vols",
# "D:\Motion_Quartet\sub-05\derivatives\func\sess-02\topup_prf\bbr\sub-05_prf_AP_undist_2vols",
# "D:\Motion_Quartet\sub-06\derivatives\func\sess-02\topup_prf\bbr\sub-06_prf_AP_undist_2vols"]
#
# VMRs = ["D:\\Motion_Quartet\\sub-01\\derivatives\\anat\\sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-03\\derivatives\\anat\\sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-04\\derivatives\\anat\\sub-04_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-05\\derivatives\\anat\\sub-05_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr",
# "D:\\Motion_Quartet\\sub-06\\derivatives\\anat\\sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr"]

FMRs = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-03\\derivatives\\func\\sess-02\\topup_prf\\bbr\\sub-03_prf_AP_undist_2vols"]

VMRs = [
"D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-03\\derivatives\\anat\\sub-03_sess-01_acq-mp2rage_UNI_denoised_IIHC.vmr"]

for it, fmr_file in enumerate(FMRs):
    docFMR = bv.open("{}.nii.gz".format(fmr_file))
    #docFMR.close()

    print("Run BBR on {}".format(fmr_file))
    #// Run BBR
    doc_vmr = bv.open(VMRs[it])
    doc_vmr = bv.active_document
    doc_vmr.coregister_fmr_to_vmr_using_bbr("{}.fmr".format(fmr_file))



print("Finished.")
