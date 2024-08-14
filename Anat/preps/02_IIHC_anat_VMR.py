
"""
Created on Tue Apr  5 15:28:35 2022
    Compute IIHC in BrinVoyager
@author: apizz

"""

import os
import glob

# =============================================================================
STUDY_PATH = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ["sub-07", "sub-08", "sub-09", "sub-10"]
SES = [1]

for su in SUBJ:
    for se in SES:
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat')
        fileVMR = glob.glob(os.path.join(PATH_IN, '*UNI_*denoised*.vmr'))[0]
        basename = fileVMR.split(os.extsep, 1)[0]

        print("Open VMR: {}".format(fileVMR))

        #// Open nifti as VMR
        docVMR = bv.open(fileVMR)
        docVMR.correct_intensity_inhomogeneities_ext(True, 3, 0.25, 0.30, 3)
        docVMR.save_as('{}_IIHC.vmr'.format(basename))
