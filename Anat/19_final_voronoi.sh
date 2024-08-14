#!/bin/bash
# Propagate VOI to 'final' GM domain

pathIn=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-10/derivatives/anat/05_ROIseg/voronoi

# # #// Second iteration (after manual work is done)
# LN2_VORONOI -init ${pathIn}/sub-01_visual_areas_hMT_LH_bvbabel.nii.gz -domain ${pathIn}/sub-01_RIM_masked_v-05_polished_GM.nii.gz -output ${pathIn}/sub-01_visual_areas_hMT_LH_bvbabel_rim_cortMask.nii.gz
# LN2_VORONOI -init ${pathIn}/sub-01_visual_areas_hMT_RH_bvbabel.nii.gz -domain ${pathIn}/sub-01_RIM_masked_v-05_polished_GM.nii.gz -output ${pathIn}/sub-01_visual_areas_hMT_RH_bvbabel_rim_cortMask.nii.gz
#
# # # Clean up boundary in case BV sampling was going outside GM
# fslmaths ${pathIn}/sub-01_visual_areas_hMT_LH_bvbabel_rim_cortMask_voronoi.nii.gz -mas ${pathIn}/sub-01_RIM_masked_v-05_polished_GM.nii.gz ${pathIn}/sub-01_visual_areas_hMT_LH_bvbabel_rim_cortMask_voronoi.nii.gz
# fslmaths ${pathIn}/sub-01_visual_areas_hMT_RH_bvbabel_rim_cortMask_voronoi.nii.gz -mas ${pathIn}/sub-01_RIM_masked_v-05_polished_GM.nii.gz ${pathIn}/sub-01_visual_areas_hMT_RH_bvbabel_rim_cortMask_voronoi.nii.gz
# # #
# # # # Remove the capsule (label: 7)
# fslmaths ${pathIn}/sub-01_visual_areas_hMT_LH_bvbabel_rim_cortMask_voronoi.nii.gz -uthr 6 ${pathIn}/sub-01_visual_areas_hMT_LH_bvbabel_rim_cortMask_voronoi_noCapsule.nii.gz
# fslmaths ${pathIn}/sub-01_visual_areas_hMT_RH_bvbabel_rim_cortMask_voronoi.nii.gz -uthr 6 ${pathIn}/sub-01_visual_areas_hMT_RH_bvbabel_rim_cortMask_voronoi_noCapsule.nii.gz
#

# #// Second iteration (after manual work is done)
# LN2_VORONOI -init ${pathIn}/sub-10_LH_visual_areas_hMT_capsule_bvbabel.nii.gz -domain ${pathIn}/sub-10_RIM_polished_mas_polished_GM.nii.gz -output ${pathIn}/sub-10_visual_areas_hMT_LH_bvbabel_rim.nii.gz
# LN2_VORONOI -init ${pathIn}/sub-10_RH_visual_areas_hMT_capsule_bvbabel.nii.gz -domain ${pathIn}/sub-10_RIM_polished_mas_polished_GM.nii.gz -output ${pathIn}/sub-10_visual_areas_hMT_RH_bvbabel_rim.nii.gz

# # Clean up boundary in case BV sampling was going outside GM
fslmaths ${pathIn}/sub-10_visual_areas_hMT_LH_bvbabel_rim_voronoi.nii.gz -mas ${pathIn}/sub-10_RIM_polished_mas_polished_GM.nii.gz ${pathIn}/sub-10_visual_areas_hMT_LH_bvbabel_rim_voronoi.nii.gz
fslmaths ${pathIn}/sub-10_visual_areas_hMT_RH_bvbabel_rim_voronoi.nii.gz -mas ${pathIn}/sub-10_RIM_polished_mas_polished_GM.nii.gz ${pathIn}/sub-10_visual_areas_hMT_RH_bvbabel_rim_voronoi.nii.gz
# #
# # # Remove the capsule (label: 7)
fslmaths ${pathIn}/sub-10_visual_areas_hMT_LH_bvbabel_rim_voronoi.nii.gz -uthr 6 ${pathIn}/sub-10_visual_areas_hMT_LH_bvbabel_rim_voronoi_noCapsule.nii.gz
fslmaths ${pathIn}/sub-10_visual_areas_hMT_RH_bvbabel_rim_voronoi.nii.gz -uthr 6 ${pathIn}/sub-10_visual_areas_hMT_RH_bvbabel_rim_voronoi_noCapsule.nii.gz
