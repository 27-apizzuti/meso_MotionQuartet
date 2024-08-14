"""Median projection across depths/layers."""

import os
import subprocess
import nibabel as nb
import numpy as np
from glob import glob

SUBJ = ['sub-01', 'sub-03', 'sub-06']

for su in SUBJ:
    PATH_FLAT = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/07_Flattening'.format(su)
    OUTDIR = os.path.join(PATH_FLAT, 'max_maps')

    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)

    os.chdir(PATH_FLAT)
    MAPS1 = glob('*phy_maps_wholeBrain*[0-9]_voronoi.nii.gz')

    print('Working on {}'.format(su))

    for i in range(len(MAPS)):
        # Determine output basename
        filename = os.path.basename(os.path.join(PATH_FLAT, MAPS[i]))
        basename, ext = filename.split(os.extsep, 1)
        outname = os.path.join(OUTDIR, "{}_max_projection.{}".format(basename, ext))

        nii = nb.load(os.path.join(PATH_FLAT, MAPS[i]))
        data = np.asarray(nii.dataobj)

        max_proj = []
        #// Separate clusters
        for it in range(0, 2):
            new_data = np.zeros(np.shape(data))
            new_data[data == it+2] = it+1
            max_proj.append(np.max(new_data, axis=2))

        max_proj2 = max_proj[0] + max_proj[1]
        # Repeat to be able to overlay on 3D flat maps
        max_proj2 = np.repeat(max_proj2[:, :, None], nii.shape[2], axis=2)

        # Save
        out = nb.Nifti1Image(max_proj2, header=nii.header, affine=nii.affine)
        nb.save(out, outname)

print('Finished.\n')
