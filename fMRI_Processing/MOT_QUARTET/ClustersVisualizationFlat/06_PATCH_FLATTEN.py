"""
Created on Thu Oct 28 14:21:14 2021
Patch Flattening script: anatomical images
NB: This script computes automatically the number of bin that should be used (x,y,z) once decided the "nominal (desired) resolution for the flattened domain"
Remeber to check the density file!!!
@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import subprocess
import math
from glob import glob

SUBJ = ['sub-01', 'sub-03', 'sub-06']
HEMI = ['LH', 'RH']
ROI = 'hMT'
NOM_RES = 0.05   # original resolution 0.2 iso mm

for iterSbj, su in enumerate(SUBJ):
    PATH_ANAT = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/06_CorticalLayers'.format(su)
    PATH_EPI = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/func/Stats/Hyph01'.format(su)
    PATH_FLAT = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/07_Flattening'.format(su)

    if not os.path.exists(PATH_FLAT):
        os.mkdir(PATH_FLAT)

    os.chdir(PATH_ANAT)
    myfile = glob('*_curvature_binned.*')[0]
    basename = myfile.split('_')
    rootname = su
    for i in range(1, len(basename)-2):
        rootname = rootname + '_' + basename[i]
    for hem in HEMI:
        # VALUES = ['/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/{}_sess-01_acq-mp2rage_UNI_denoised_IIHC_res2x_v16_bvbabel_SS.nii.gz'.format(su, su),
        #             os.path.join(PATH_ANAT, '{}_curvature_binned.nii.gz'.format(rootname)),
        #             os.path.join(PATH_EPI, '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_UVD_max_filter_plus1.nii.gz'.format(su, hem, ROI))]
        # VALUES = [os.path.join(PATH_ANAT, '{}_curvature_binned.nii.gz'.format(rootname)),
        #             os.path.join(PATH_EPI, '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_UVD_max_filter_plus1.nii.gz'.format(su, hem, ROI))]
        VALUES = [os.path.join(PATH_EPI, '{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_UVD_max_filter_ambiguous_mask_plus1.nii.gz'.format(su, hem, ROI))]
        os.chdir(PATH_ANAT)
        mycoord_uv = glob('*_{}_{}_UV_coordinates*'.format(ROI, hem))[0]
        myperi = glob('*_{}_{}_perimeter_chunk*'.format(ROI, hem))[0]

        COORD_UV = os.path.join(PATH_ANAT, '{}'.format(mycoord_uv))
        COORD_D = os.path.join(PATH_ANAT,'{}_metric_equivol.nii.gz'.format(rootname))
        DOMAIN = os.path.join(PATH_ANAT, '{}'.format(myperi))

        # 1) Find the cortical thickness of the disk
        NII_FILE1 = os.path.join(PATH_ANAT, '{}_thickness.nii.gz'.format(rootname))
        nii1 = nb.load(NII_FILE1)
        thick = np.asarray(nii1.dataobj)
        thick = np.multiply(thick, 0.35)

        NII_FILE2 = os.path.join(PATH_ANAT, '{}'.format(myperi))
        nii2 = nb.load(NII_FILE2)
        mask = np.asarray(nii2.dataobj)
        chunk_thick = np.mean(thick[mask > 0])
        print('Average cortical thickness of the chunk: {}'.format(chunk_thick))
        binZ = 2 * math.ceil( chunk_thick / NOM_RES )
        if binZ % 2 == 0:
            binZ = binZ + 1
        #
        # 2) Find binX, binY
        # Find RADIUS of each disk from the filename
        temp = mycoord_uv.split('_')
        RADIUS = np.multiply(int(temp[-5]), 0.35)
        chunk_area = math.pi * (RADIUS*RADIUS)
        binX = math.ceil( math.sqrt(chunk_area / (NOM_RES*NOM_RES)) )
        print('BinZ {}, BinX {}'.format(binZ, binX))
        #
        for j, values in enumerate(VALUES):
            # Determine output basename
            filename = os.path.basename(values)
            basename, ext = filename.split(os.extsep, 1)
            outname = os.path.join(PATH_FLAT, "{}_{}_{}.{} ".format(basename, ROI, hem, ext))
            print(outname)
            print('Flattening {}'.format(filename))

            command = "LN2_PATCH_FLATTEN "
            command += "-values {} ".format(values)
            command += "-coord_uv {} ".format(COORD_UV)
            command += "-coord_d {} ".format(COORD_D)
            command += "-domain {} ".format(DOMAIN)
            command += "-bins_u {} ".format(binX)
            command += "-bins_v {} ".format(binX)
            command += "-bins_d {} ".format(binZ)
            command += "-voronoi -norm_mask "
            command += "-density "
            command += "-output {} ".format(outname)
            subprocess.run(command, shell=True)
