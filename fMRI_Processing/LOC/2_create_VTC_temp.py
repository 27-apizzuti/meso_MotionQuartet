# preprocess FMR: slictime, moco, highpass ; AP
# This script was used to preprocess high-res and lo-res functional data acquired with CMRR sequence;

import numpy as np
import os
import glob

print("Hello.")

# =============================================================================


FMR = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-09\\derivatives\\func\\sess-01\\loc01\\sub-09_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_warped_THPGLMF3c.fmr"]

IA_TRX = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-09\\derivatives\\func\\sess-01\\loc01\\BBR\\sub-09_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_warped_THPGLMF3c-TO-sub-09_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_IA.trf"]

FA_TRX = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-09\\derivatives\\func\\sess-01\\loc01\\BBR\\sub-09_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_warped_THPGLMF3c-TO-sub-09_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_BBR_FA.trf"]

VTC = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-09\\derivatives\\func\\sess-01\\loc01\\GLM\\sub-09_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_warped_THPGLMF3c.vtc"]

VMR = ["D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD\\sub-09\\derivatives\\anat\\sub-09_sess-02_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.vmr"]

for it, fmr_file in enumerate(FMR):

    #// Open VMR
    file_vmr = VMR[it]
    doc_vmr = bv.open(file_vmr)

    #// Input files
    fmr_file = FMR[it]
    coreg_fa_trf_file = FA_TRX[it]
    coreg_ia_trf_file = IA_TRX[it]

    #// Output name
    vtc_file = VTC[it]
    doc_vmr.create_vtc_in_native_space(fmr_file, coreg_ia_trf_file, coreg_fa_trf_file, vtc_file, 1, 1)
    #// 2 means we are using sinc interpolation
