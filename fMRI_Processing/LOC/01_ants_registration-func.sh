#!/bin/bash
# Non Linear Coregistration (Syn, by ANTs)
#
# Input files: 1. Target, 2. Source 3. initial_matrix_ITK.txt (manual+rigid+affine, by ITK-SNAP) 4. mask.nii around ROI
# No mask option used for P04 and P03 P02 (anat alignment), P05
echo "I expect 2 filed: target file (e.g. high-res T1w from VASO) and a moving (or source) file"
echo " Co-registration-part II: Source to Target ----> Syn [ANTs]"

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=2
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

# 1. FUNC sess-02 to FUNC sess-01
mysub=sub-09
mydata=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/${mysub}/derivatives/func/sess-01/loc01/02_ANTS
myTarget=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/${mysub}/derivatives/func/sess-01/loc01/02_ANTS/${mysub}_task-prf_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_reference_bvbabel.nii.gz
mySource=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/${mysub}/derivatives/func/sess-01/loc01/02_ANTS/${mysub}_task-loc_acq-2depimb2_run-01_SCSTBL_3DMCTS_reference_bvbabel.nii.gz

myITK=${mydata}/initial_affine.txt

# Create output folder
cd ${mydata}

#===========================================
# Coregistration done in 2 steps
echo "*****************************************"
echo "************* starting with ANTS ********"
echo "*****************************************"

antsRegistration \
--verbose 1 \
--dimensionality 3 \
--float 1 \
--output [${mydata}/registered_,${mydata}/registered_Warped.nii.gz,${mydata}/registered_InverseWarped.nii.gz] \
--interpolation BSpline[5] \
--use-histogram-matching 0 \
--winsorize-image-intensities [0.005,0.995] \
--transform Rigid[0.05] \
--metric MI[${myTarget},${mySource},0.7,32,Regular,0.1] \
--convergence [1000x500,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox \
--transform Affine[0.1] \
--metric MI[${myTarget},${mySource},0.7,32,Regular,0.1] \
--convergence [1000x500,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox \
--initial-moving-transform ${myITK} \
--transform SyN[0.1,2,0] \
--metric CC[${myTarget},${mySource},1,2] \
--convergence [500x100,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox
# -x mask.nii.gz


antsApplyTransforms -d 3 -i ${mySource} -o ${mysub}_loc_anat_resliced_prf.nii.gz -r ${myTarget} -t ${mydata}/registered_1Warp.nii.gz -t ${mydata}/registered_0GenericAffine.mat
antsApplyTransforms -d 3 -i ${mySource} -o ${mysub}_loc_anat_resliced_loc.nii.gz -r ${mySource} -t ${mydata}/registered_1Warp.nii.gz -t ${mydata}/registered_0GenericAffine.mat
