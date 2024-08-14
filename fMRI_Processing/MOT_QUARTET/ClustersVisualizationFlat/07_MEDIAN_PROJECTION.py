"""Median projection across depths/layers."""

import os
import subprocess
import nibabel as nb
import numpy as np
from glob import glob

SUBJ = ['sub-01']

for su in SUBJ:
    PATH_FLAT = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/07_Flattening'.format(su)
    OUTDIR = os.path.join(PATH_FLAT, 'median_maps')

    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)

    os.chdir(PATH_FLAT)
    MAPS = glob('*curvature_binned*[0-9]_voronoi.nii.gz')
    #-----------------------------------------------------------------------------

    for i in range(len(MAPS)):
        # Determine output basename
        filename = os.path.basename(os.path.join(PATH_FLAT, MAPS[i]))
        basename, ext = filename.split(os.extsep, 1)
        outname = os.path.join(OUTDIR, "{}_median_projection.{}".format(basename, ext))

        nii = nb.load(os.path.join(PATH_FLAT, MAPS[i]))
        data = np.asarray(nii.dataobj)

        data = np.median(data, axis=2)

        # Repeat to be able to overlay on 3D flat maps
        data = np.repeat(data[:, :, None], nii.shape[2], axis=2)

        # Save
        out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
        nb.save(out, outname)

print('Finished.\n')
