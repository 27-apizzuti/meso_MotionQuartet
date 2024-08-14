#!/bin/bash
# Propagate VOI to GM domain

pathIn=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-07/derivatives/anat/06_CorticalLayers

#// RIM POLISH
LN2_RIM_POLISH -rim ${pathIn}/sub-07_RIM_polished_mas_v-03_polished.nii.gz

#// Create only GM
# fslmaths ${pathIn}/sub-06_RIM_ZOOM_v-03_polished.nii.gz -thr 3 ${pathIn}/sub-06_RIM_ZOOM_v-03_polished_GM.nii.gz
