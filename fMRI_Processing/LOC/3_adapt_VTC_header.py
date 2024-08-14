# This script adapts the header of the VTC by allowing to map to VMR with double res. 0.35 iso mm

import numpy as np
import os
import glob
import bvbabel

print("Hello.")

# =============================================================================
STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-09"]
SESS = ["sess-01"]

for su in SUBJ:
    for se in SESS:
        print('Working on {}, {}'.format(su, se))
        PATH_VTC = os.path.join(STUDY_PATH, su, 'derivatives', 'func', se, 'loc01')
        file_vtc = glob.glob(os.path.join(PATH_VTC, 'GLM', '*.vtc'))[0]

        #// Change output name
        basename = file_vtc.split(os.extsep, 1)[0]
        outname = basename.split("/")[-1]
        output_file = os.path.join(PATH_VTC, "{}_res2x.vtc".format(outname, se))

        #// Adjust header with double resolution
        print('Create secondary VTC with adapted header to 2x')
        outname = os.path.join(PATH_VTC, "{}_{}_BBR_resx2.vtc".format(outname, se))

        header, data = bvbabel.vtc.read_vtc(file_vtc, rearrange_data_axes=False)
        header["VTC resolution relative to VMR (1, 2, or 3)"] = 2
        header["XEnd"] = header["XEnd"] *2
        header["XStart"] = header["XStart"] *2

        header["YEnd"] = header["YEnd"]*2
        header["YStart"] = header["YStart"] *2

        header["ZEnd"] = header["ZEnd"] *2
        header["ZStart"] = header["ZStart"] *2
        bvbabel.vtc.write_vtc(output_file, header, data, rearrange_data_axes=False)
