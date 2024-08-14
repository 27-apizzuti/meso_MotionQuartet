#!/bin/bash
# Propagate VOI to GM domain

pathIn=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-04/derivatives/anat/05_ROI_seg

# Remove the capsule (label: 7)
# fslmaths ${pathIn}/sub-04_visual_areas_hMT_RH_bvbabel_rim_voronoi_bin_noCapsule_dilated.nii.gz -add ${pathIn}/sub-04_visual_areas_hMT_LH_bvbabel_rim_voronoi_bin_noCapsule_dilated.nii.gz -bin ${pathIn}/sub-04_LH_RH_dilated.nii.gz
fslmaths ${pathIn}/sub-04_RIM_kenshu.nii.gz -mas ${pathIn}/sub-04_LH_RH_dilated.nii.gz ${pathIn}/sub-04_RIM_ZOOM_kenshu.nii.gz
