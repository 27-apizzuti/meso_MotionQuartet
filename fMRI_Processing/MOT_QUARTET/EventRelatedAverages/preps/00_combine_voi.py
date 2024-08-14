"""Convert BrainVoyager VOI files into VTC sized Nifti files.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import bvbabel
import numpy as np
import nibabel as nb
from pprint import pprint

# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-09', 'sub-08', 'sub-10']
# =============================================================================
for su in SUBJ:
    
    # Voxels of interest
    FILES_VOI = ["/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_V1_LH_Horizontal_layers_equivol.voi".format(su, su),
    "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_V1_RH_Horizontal_layers_equivol.voi".format(su, su),

    "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_V1_LH_Vertical_layers_equivol.voi".format(su, su),
    "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_V1_RH_Vertical_layers_equivol.voi".format(su, su),

    "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_hMT_LH_Horizontal_layers_equivol.voi".format(su, su),
    "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_hMT_RH_Horizontal_layers_equivol.voi".format(su, su),

    "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_hMT_LH_Vertical_layers_equivol.voi".format(su, su),
    "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers/physical_VOI/{}_hMT_RH_Vertical_layers_equivol.voi".format(su, su)]

    TEMPLATE_VOI = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/template_4ROIS.voi"
    OUTDIR = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/carpet-amb".format(su)

    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)
   
    print('Working on {} \n'.format(su))
    # -----------------------------------------------------------------------------
    # Step 1: Load template voi
    header_templ, data_templ = bvbabel.voi.read_voi(TEMPLATE_VOI)
    nr_vois = len(FILES_VOI)

    # Step 2: Load each voi
    for it, voi in enumerate(range(0, nr_vois, 2)):
        print('Loading: {} {} \n'.format(FILES_VOI[voi], FILES_VOI[voi+1]))
        # Read both hemispheres
        header_voi_LH, data_voi_LH = bvbabel.voi.read_voi(FILES_VOI[voi])
        header_voi_RH, data_voi_RH = bvbabel.voi.read_voi(FILES_VOI[voi+1])

        # Merge layers - first three VOIs
        roi_data = np.concatenate((data_voi_LH[0]["Coordinates"], data_voi_RH[0]["Coordinates"],
                   data_voi_LH[1]["Coordinates"], data_voi_RH[1]["Coordinates"],
                   data_voi_LH[2]["Coordinates"], data_voi_RH[2]["Coordinates"]), axis=0)

        print('Number of coord {} == {}'.format(data_voi_LH[0]["Coordinates"].shape, data_voi_LH[0]["NrOfVoxels"]))

        nr_vox = (data_voi_LH[0]["NrOfVoxels"] + data_voi_LH[1]["NrOfVoxels"] + data_voi_LH[2]["NrOfVoxels"]
                  + data_voi_RH[0]["NrOfVoxels"] + data_voi_RH[1]["NrOfVoxels"] + data_voi_RH[2]["NrOfVoxels"])

        # Fill template VOI 
        data_templ[it]["Coordinates"] = np.asarray(roi_data)
        data_templ[it]["NrOfVoxels"] = nr_vox
        print('Number of coor {} == {}'.format(data_templ[it]["Coordinates"].shape, data_templ[it]["NrOfVoxels"] ))

    #// Save new VOI
    print('Save new VOI ------------------------- \n')
    outname = os.path.join(OUTDIR, '{}_combined_4ROIs.voi'.format(su))
    bvbabel.voi.write_voi(outname, header_templ, data_templ)

print("\nFinished.")
