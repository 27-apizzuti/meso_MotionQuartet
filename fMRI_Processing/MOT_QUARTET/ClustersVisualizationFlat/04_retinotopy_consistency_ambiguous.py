"""(Exploratory) Check: compare physical and ambiguous congruency in best retinotopic V1 voxels defined with physical motion."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
import matplotlib.pyplot as plt

SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
HEMI = ['RH']
ROI = ['hMT', 'V1']

my_dpi = 96
fig, ax = plt.subplots(figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
congr = np.zeros([len(ROI), len(SUBJ), 2])       # roi, subjects, (horizontal and vertical)

for itro, ro in enumerate(ROI):
    for itsu, su in enumerate(SUBJ):

        PATH_IN = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/'.format(su)

        # Load t-map from ambiguous motion
        FILENAME = '{}_Amb_maps_wholeBrain_bvbabel_res2x_float32.nii.gz'.format(su)
        FILE = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Amb', FILENAME)
        niimap = nb.load(FILE)
        amb = np.asarray(niimap.dataobj)
        amb = amb[..., 0]

        # Load t-map from physical motion
        FILENAME = '{}_Phy_maps_wholeBrain_bvbabel_res2x_float32.nii.gz'.format(su)
        FILE = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Phy', FILENAME)
        niimap = nb.load(FILE)
        phy = np.asarray(niimap.dataobj)
        phy = phy[..., 0]

        for hem in HEMI:

            print('Working on {} {} {}'.format(su, hem, ro))
            FILENAMES = ['{}_phy_maps_wholeBrain_bvbabel_res2x_float32_clusters_{}_{}_UVD_max_filter.nii.gz'.format(su, hem, ro)]

            for file in FILENAMES:
                FILENII = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Hyph01', file)
                PATH_OUT = os.path.join(PATH_IN, 'derivatives', 'func', 'Stats', 'Hyph01')
                basename, ext = FILENII.split(os.extsep, 1)
                niiclu = nb.load(FILENII)
                clu = np.asarray(niiclu.dataobj)
                hor = clu == 1
                ver = clu == 2

                # New data
                new_mask = np.zeros(np.shape(clu))

                #// Count number of voxels that are sign congruent
                x1 = phy[hor] > 0
                x2 = phy[ver] < 0

                y1 = amb[hor] > 0
                y2 = amb[ver] < 0
                print('File: {} '.format(file))
                print('Physical motion, horizontal congruence: {}/{} ({}%)'.format(np.sum(hor>0), np.sum(x1), (np.sum(x1)/np.sum(hor>0))*100 ))
                print('Physical motion, vertical congruence: {}/{} ({}%)'.format(np.sum(ver>0), np.sum(x2), (np.sum(x2)/np.sum(ver>0))*100 ))

                print('Ambiguous motion, horizontal congruence: {}/{} ({}%)'.format(np.sum(hor>0), np.sum(y1), (np.sum(y1)/np.sum(hor>0))*100 ))
                print('Ambiguous motion, vertical congruence: {}/{} ({}%)'.format(np.sum(ver>0), np.sum(y2), (np.sum(y2)/np.sum(ver>0))*100 ))
                print('*****************************************************************')
                congr[itro, itsu, 0] = (np.sum(y1)/np.sum(hor>0))*100
                congr[itro, itsu, 1] = (np.sum(y2)/np.sum(ver>0))*100

                #// Save voxels selection based on ambiguous motion
                new_mask[hor*(amb>0)] = 1
                new_mask[ver*(amb<0)] = 2

                OUTPUTNAME = os.path.join(PATH_OUT, '{}_ambiguous_mask.nii.gz'.format(basename))
                img = nb.Nifti1Image(new_mask, affine=niimap.affine, header=niimap.header)
                nb.save(img, OUTPUTNAME)

# Group-level statistics
V1 = np.mean(np.mean(congr[1, :, :]))
hMT = np.mean(np.mean(congr[0, :, :]))

print('Congruency average across subjects for {} V1 = {}'.format(hem, V1))
print('Congruency average across subjects for {} hMT = {}'.format(hem, hMT))
