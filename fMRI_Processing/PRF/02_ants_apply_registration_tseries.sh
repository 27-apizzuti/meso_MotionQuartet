#!/bin/bash
# Reslicing (Syn, by ANTs)
#
# Input files: 1. Time series processed, 2. Transformation matrices (/alignment_ANTs folder)

# Check mySource file: it can be distoreted (P02) or undistored (P03, P04)

echo " Co-registration-part III: Reslicing time series ----> Source to Target   [ANTs]"

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

mysub=sub-01
mymain=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-01/derivatives/func/sess-02
ants_path=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-01/derivatives/func/sess-02/ANTS-BBR

cd ${ants_path}

# # Time series resampling
# echo 'Apply ants to amb01'
# antsApplyTransforms -d 3 -e 3 -i ${mymain}/amb01/topup/sub-01_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist.nii.gz -o ${mymain}/amb01/topup/sub-01_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_warped.nii.gz -r sub-01_sess-01_acq-2depimb2_ref_01_undist.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
#
# echo 'Apply ants to amb02'
# antsApplyTransforms -d 3 -e 3 -i ${mymain}/amb02/topup/sub-01_task-amb_acq-2depimb2_run-02_SCSTBL_3DMCTS_bvbabel_undist.nii.gz -o ${mymain}/amb02/topup/sub-01_task-amb_acq-2depimb2_run-02_SCSTBL_3DMCTS_bvbabel_undist_warped.nii.gz -r sub-01_sess-01_acq-2depimb2_ref_01_undist.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
#
# echo 'Apply ants to amb03'
# antsApplyTransforms -d 3 -e 3 -i ${mymain}/amb03/topup/sub-01_task-amb_acq-2depimb2_run-03_SCSTBL_3DMCTS_bvbabel_undist.nii.gz -o ${mymain}/amb03/topup/sub-01_task-amb_acq-2depimb2_run-03_SCSTBL_3DMCTS_bvbabel_undist_warped.nii.gz -r sub-01_sess-01_acq-2depimb2_ref_01_undist.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
#
# echo 'Apply ants to phy01'
# antsApplyTransforms -d 3 -e 3 -i ${mymain}/phy01/topup/sub-01_task-phy_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist.nii.gz -o ${mymain}/phy01/topup/sub-01_task-phy_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_warped.nii.gz -r sub-01_sess-01_acq-2depimb2_ref_01_undist.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
#
# echo 'Apply ants to phy02'
# antsApplyTransforms -d 3 -e 3 -i ${mymain}/phy02/topup/sub-01_task-phy_acq-2depimb2_run-02_SCSTBL_3DMCTS_bvbabel_undist.nii.gz -o ${mymain}/phy02/topup/sub-01_task-phy_acq-2depimb2_run-02_SCSTBL_3DMCTS_bvbabel_undist_warped.nii.gz -r sub-01_sess-01_acq-2depimb2_ref_01_undist.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
# #
echo 'Apply ants to phy03'
antsApplyTransforms -d 3 -e 3 -i ${mymain}/phy03/topup/sub-01_task-phy_acq-2depimb2_run-03_SCSTBL_3DMCTS_bvbabel_undist.nii.gz -o ${mymain}/phy03/topup/sub-01_task-phy_acq-2depimb2_run-03_SCSTBL_3DMCTS_bvbabel_undist_warped.nii.gz -r sub-01_sess-01_acq-2depimb2_ref_01_undist.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

echo 'Apply ants to phy04'
antsApplyTransforms -d 3 -e 3 -i ${mymain}/phy04/topup/sub-01_task-phy_acq-2depimb2_run-04_SCSTBL_3DMCTS_bvbabel_undist.nii.gz -o ${mymain}/phy04/topup/sub-01_task-phy_acq-2depimb2_run-04_SCSTBL_3DMCTS_bvbabel_undist_warped.nii.gz -r sub-01_sess-01_acq-2depimb2_ref_01_undist.nii.gz -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
