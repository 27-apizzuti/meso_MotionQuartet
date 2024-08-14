#!/bin/bash
# This script is used to extract the brain for MP2RAGE anatomy and to create a brainmask
# P04, P03, P02, P05, P06
# 1. Use INV2 to extract the brain (bet or afni) --> skull stripped
# 2. Apply brain mask to UNI_reg

pathIn=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat

#//0. Correct for inhomogeneities
# N4BiasFieldCorrection -i ${pathIn}/sub-06_sess-01_acq-mp2rage_inv2.nii -o ${pathIn}/sub-06_sess-01_acq-mp2rage_inv2_BFC.nii.gz

# #//1. Compute brainmask
# 3dAutomask -prefix ${pathIn}/mask.nii -peels 3 -dilate 2 -overwrite ${pathIn}/sub-06_sess-01_acq-mp2rage_inv2_BFC.nii.gz
# bet ${pathIn}/sub-06_sess-01_acq-mp2rage_inv2_BFC.nii.gz ${pathIn}/mask_bet.nii.gz -m -R -f 0.03

#//2. Apply brainmask
fslmaths ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel.nii.gz -mas ${pathIn}/sub-06_brainmask_polished.nii.gz ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS.nii.gz
# fslmaths ${pathIn}/sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_v16_bvbabel.nii.gz -mas ${pathIn}/sub-01_brainmask.nii ${pathIn}/sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_v16_bvbabel_SS.nii.gz

#//3. Correct again
N4BiasFieldCorrection -i ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS.nii.gz -o ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC.nii.gz
