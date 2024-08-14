"""
Created on Thu Oct 28 14:21:14 2021
Patch Flattening
Remove numbers from the filename
@author: apizz
"""
import re
import os
from glob import glob

SUBJ = ['sub-01']

for iterSbj, su in enumerate(SUBJ):
    PATH_FLAT = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/derivatives/anat/07_Flattening'.format(su)

    os.chdir(PATH_FLAT)
    myfiles = glob('*voronoi*')

    for file_name in myfiles:
        os.rename(file_name, file_name.translate(str.maketrans('','','0123456789'))

        print(file_name)
        print(new_name)

print('Success.')
