#!/bin/bash
# Propagate VOI to GM domain

pathIn=/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/sub-04/derivatives/anat/04_CorticalMask

#// Separate GM from WMGM nifti (from BrainVoyaer)
# fslmaths ${pathIn}/sub-04_GM_bvbabel.nii.gz -uthr 101 -bin ${pathIn}/sub-04_GM.nii.gz

#// First iteration (from VOI Brainvoyager, then next step is to create the dilated version of the region and afterwards do manual segmentation)
# LN2_VORONOI -init ${pathIn}/sub-04_LH_visual_areas_hMT_bvbabel.nii.gz -domain ${pathIn}/sub-04_GM.nii.gz -output ${pathIn}/sub-04_visual_areas_hMT_LH_bvbabel_rim.nii.gz
LN2_VORONOI -init ${pathIn}/sub-04_RH_visual_areas_hMT_bvbabel.nii.gz -domain ${pathIn}/sub-04_GM.nii.gz -output ${pathIn}/sub-04_visual_areas_hMT_RH_bvbabel_rim.nii.gz
# LN2_VORONOI -init ${pathIn}/sub-01_GM_bvbabel.nii.gz -domain ${pathIn}/sub-01_sess-02_brainmask_res2x_bvbabel_thr.nii.gz -output ${pathIn}/sub-01_sess-02_brainmask_res2x_bvbabel_thr.nii.gz

# # Clean up boundary in case BV sampling was going outside GM
# fslmaths ${pathIn}/sub-04_visual_areas_hMT_LH_bvbabel_rim_voronoi.nii.gz -mas ${pathIn}/sub-04_GM.nii.gz ${pathIn}/sub-04_visual_areas_hMT_LH_bvbabel_rim_voronoi.nii.gz
fslmaths ${pathIn}/sub-04_visual_areas_hMT_RH_bvbabel_rim_voronoi.nii.gz -mas ${pathIn}/sub-04_GM.nii.gz ${pathIn}/sub-04_visual_areas_hMT_RH_bvbabel_rim_voronoi.nii.gz

# Remove the capsule (label: 7)
# fslmaths ${pathIn}/sub-04_visual_areas_hMT_LH_bvbabel_rim_voronoi.nii.gz -uthr 6 -bin ${pathIn}/sub-04_visual_areas_hMT_LH_bvbabel_rim_voronoi_bin_noCapsule.nii.gz
fslmaths ${pathIn}/sub-04_visual_areas_hMT_RH_bvbabel_rim_voronoi.nii.gz -uthr 6 -bin ${pathIn}/sub-04_visual_areas_hMT_RH_bvbabel_rim_voronoi_bin_noCapsule.nii.gz

#// Second iteration (after manual work is done)
# LN2_VORONOI -init ${pathIn}/sub-04_LH_visual_areas_hMT_bvbabel.nii.gz -domain ${pathIn}/sub-04_GM.nii.gz -output ${pathIn}/sub-04_visual_areas_hMT_LH_bvbabel_rim.nii.gz
# LN2_VORONOI -init ${pathIn}/sub-04_RH_visual_areas_hMT_bvbabel.nii.gz -domain ${pathIn}/sub-04_GM.nii.gz -output ${pathIn}/sub-04_visual_areas_hMT_RH_bvbabel_rim.nii.gz
