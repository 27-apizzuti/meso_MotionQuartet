"""
Created on Thu May 26 15:37:23 2022
This script evaluates the behavioral data from fMRI sessions and it creates PRT file in VOLUMES.
Each trigger is considered as a volume.
For the localizer stimulus.

CHECK DURATION ARRAY FOR EACH PARTICIPANT

@author: apizz
"""

import pandas as pd
import numpy as np
import glob
import os

PATH_IN = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ['sub-06']
Conditions = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
Durations = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
 10, 10, 10])

N_COND = len(Conditions)
FILE_NAME = 'Protocol_{}_Localizer_Run01.prt'.format(SUBJ[0])
PATH_OUT = os.path.join(PATH_IN)

# // Write protocol file
prtName = os.path.join(PATH_OUT, FILE_NAME)
file = open(prtName, 'w')
header = ['FileVersion: 2\n',
'ResolutionOfTime: Volumes\n',
'Experiment: Localizer\n',
'BackgroundColor: 0 0 0\n',
'TextColor: 255 255 202\n',
'TimeCourseColor: 255 255 255\n',
'TimeCourseThick: 3\n',
'ReferenceFuncColor: 192 192 192\n',
'ReferenceFuncThick: 2\n'
'NrOfConditions: 2\n'
]

file.writelines(header)

CumDurations = np.cumsum(Durations)
Labels = ['Static', 'Center']
Colors = ['Color: 192 192 192', 'Color: 255 0 0']
unique_conditions = np.array([0, 1])

for it, cond in enumerate(unique_conditions):

    idx =  np.asarray(np.where(Conditions == cond))
    file.writelines(['\n{}\n{}\n'.format(Labels[it], np.shape(idx)[1])])

    for myiter in range(0, np.shape(idx)[1]):
        if idx[0][myiter] == 0:
            start = 1
        else:
            start = CumDurations[idx[0][myiter]-1] + 1
        end = CumDurations[idx[0][myiter]]
        file.writelines(['{} {}\n'.format(start, end)])
    file.writelines(['{}\n'.format(Colors[it])])

file.close()
print("Success.")
