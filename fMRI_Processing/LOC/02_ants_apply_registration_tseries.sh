#!/bin/bash
# Reslicing (Syn, by ANTs)
#
# Input files: 1. Time series processed, 2. Transformation matrices (/alignment_ANTs folder)

# Check mySource file: it can be distoreted (P02) or undistored (P03, P04)

echo " Co-registration-part III: Reslicing time series ----> Source to Target   [ANTs]"

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

mysub=sub-09
mymain=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-09/derivatives/func/sess-01
ants_path=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-09/derivatives/func/sess-01/loc01/02_ANTS

cd ${ants_path}

# # Time series resampling

echo 'Apply ants to loc01'
antsApplyTransforms -d 3 -e 3 -i ${ants_path}/sub-09_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel.nii.gz -o ${ants_path}/sub-09_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_warped.nii.gz -r ${ants_path}/sub-09_task-prf_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_reference_bvbabel.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
