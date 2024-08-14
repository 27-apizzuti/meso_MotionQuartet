#!/bin/bash
# This script is used to apply a subcortical mask

pathIn=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-06/derivatives/anat/02_AdvSeg

#//1. Binarize subcortical mask (225: subcortex)
# fslmaths ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_ISO_ACPC_bvbabel.nii.gz -thr 225 -bin ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_ISO_ACPC_bvbabel_mask.nii.gz
# fslmaths ${pathIn}/sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_v16_bvbabel.nii.gz -mas ${pathIn}/sub-01_brainmask.nii ${pathIn}/sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_v16_bvbabel_SS.nii.gz

#2// Extract cerebellum mask
# fslmaths ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_ISO_ACPC_beforeMask_bvbabel.nii.gz -sub ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_ISO_ACPC_bvbabel.nii.gz ${pathIn}/test.nii.gz
# fslmaths ${pathIn}/test.nii.gz -thr 100 -bin ${pathIn}/test2.nii.gz

#// Binarize GM from BrainVoyager
# fslmaths ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x_ETC-7x-R5_WM_bvbabel.nii.gz -thr 240 ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x_ETC-7x-R5_WM_bvbabel_bin.nii.gz

#// Split hemispheres
fslmaths ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x_ETC-7x-R5_WM_bvbabel_bin_v01_polished_SPLIT.nii.gz -thr 2 -bin ${pathIn}/sub-06_LH_WM.nii.gz
fslmaths ${pathIn}/sub-06_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SS_BFC_Nocereb_subcort_res2x_ETC-7x-R5_WM_bvbabel_bin_v01_polished_SPLIT.nii.gz -uthr 1 -bin ${pathIn}/sub-06_RH_WM.nii.gz
