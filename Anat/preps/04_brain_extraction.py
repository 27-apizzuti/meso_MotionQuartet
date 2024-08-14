"""Read BrainVoyager vmr and export nifti."""


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
import subprocess

STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-09"]
SES = [2]

for su in SUBJ:
    for se in SES:
        print('Working on {}'.format(su))
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat')

        FILE1 = os.path.join(STUDY_PATH, su, 'sourcedata', 'sess-0{}'.format(se), 'NIFTI', 'anat', '{}_sess-0{}_acq-mp2rage_inv2.nii'.format(su, se))
        FILE2 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_UNI_denoised_IIHC_bvbabel.nii.gz'.format(su, se))

        OUT1 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_inv2_BFC.nii.gz'.format(su, se))
        OUT2 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_UNI_denoised_IIHC_bvbabel_BFC.nii.gz'.format(su, se))
        print('Running N4BiasFieldCorrection for INV2')

        #//0. Correct for inhomogeneities
        command = "N4BiasFieldCorrection -i {} ".format(FILE1)
        command += "-o {} ".format(OUT1)
        print(command)
        subprocess.run(command, shell=True)


        # #//1. Compute brainmask
        print('Computing brainmask with AFNI')
        OUTAFNI = os.path.join(PATH_IN, '{}_sess-0{}_mask_afnii.nii.gz'.format(su, se))
        command = "3dAutomask -prefix {} ".format(OUTAFNI)
        command += "-peels 3 -dilate 2 -overwrite {} ".format(OUT1)
        subprocess.run(command, shell=True)

        print('Computing brainmask with BET')
        OUTBET = os.path.join(PATH_IN, '{}_sess-0{}_mask_bet.nii.gz'.format(su, se))
        command = "bet {} {} ".format(OUT1, OUTBET)
        command += "-m -R -f 0.03 "
        subprocess.run(command, shell=True)

        #//2. Apply brainmask
        print('Apply brainmask')
        OUT3 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSafni.nii.gz'.format(su, se))
        OUT4 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet.nii.gz'.format(su, se))
        command = "fslmaths {} -mas {} {} ".format(FILE2, OUTAFNI, OUT3)
        print(command)
        subprocess.run(command, shell=True)

        OUTBET = os.path.join(PATH_IN, '{}_sess-0{}_mask_bet_mask.nii.gz'.format(su, se))
        command = "fslmaths {} -mas {} {} ".format(FILE2, OUTBET, OUT4)
        subprocess.run(command, shell=True)

        #//3 Correct for inhomogeneities
        print('Running N4BiasFieldCorrection for brainmasked UNI')

        OUT5 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSafni_BFC.nii.gz'.format(su, se))
        OUT6 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC.nii.gz'.format(su, se))
        command = "N4BiasFieldCorrection -i {} ".format(OUT3)
        command += "-o {} ".format(OUT5)
        subprocess.run(command, shell=True)

        command = "N4BiasFieldCorrection -i {} ".format(OUT4)
        command += "-o {} ".format(OUT6)
        subprocess.run(command, shell=True)

print("Finished.")
