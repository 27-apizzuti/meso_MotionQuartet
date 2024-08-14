"""
Created on Thu May 26 15:37:23 2022
This script evaluates the behavioral data from fMRI sessions and it creates PRT file in VOLUMES.
Each trigger is considered as a volume.
For the unambiguous stimulus.

CHECK DURATION ARRAY FOR EACH PARTICIPANT

@author: apizz
"""

import pandas as pd
import numpy as np
import glob
import os

PATH_IN = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ['sub-01']
SESS = [3]

Conditions = np.array([0, 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 3,
 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 3, 0])

Durations = np.array([20, 10, 10, 10, 10, 10, 10, 10, 10, 16, 10, 10, 10, 10, 10, 10, 10, 10, 16, 10, 10, 10, 10, 10,
 10, 10, 10, 16, 10, 10, 10, 10, 10, 10, 10, 10, 16, 10, 10, 10, 10, 10, 10, 10, 10, 16, 10, 10,
 10, 10, 10, 10, 10, 10, 16, 20])

N_COND = len(Conditions)
FILE_NAME = 'Protocol_{}_Exp2_unamb_MotQuart_Run01.prt'.format(SUBJ[0])
PATH_OUT = os.path.join(PATH_IN, SUBJ[0], 'Protocols', 'sess-0{}'.format(SESS[0]), 'Exp1_Phys_MotQuart', 'Protocols')

# // Create Condition-start and end point


# // Write protocol file
prtName = os.path.join(PATH_OUT, FILE_NAME)
file = open(prtName, 'w')
header = ['FileVersion: 2\n',
'ResolutionOfTime: Volumes\n',
'Experiment: Exp1_unambiguousMotion\n',
'BackgroundColor: 0 0 0\n',
'TextColor: 255 255 202\n',
'TimeCourseColor: 255 255 255\n',
'TimeCourseThick: 3\n',
'ReferenceFuncColor: 192 192 192\n',
'ReferenceFuncThick: 2\n'
'NrOfConditions: 4\n'
]

file.writelines(header)

CumDurations = np.cumsum(Durations)
Labels = ['Fixation', 'Horizontal', 'Vertical', 'Baseline']
Colors = ['Color: 64 64 64', 'Color: 255 0 0', 'Color: 0 255 0', 'Color: 150 150 150']
unique_conditions = np.array([0, 1, 2, 3])

for it, cond in enumerate(unique_conditions):
    if it == 0:
        idx = np.asarray(np.where(Conditions == 0))
        file.writelines(['\nFixation\n{}\n'.format(np.shape(idx)[1])])
    else:
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
