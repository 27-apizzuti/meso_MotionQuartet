"""
Created on Thu May 26 15:37:23 2022
This script evaluates the behavioral data from fMRI sessions and it creates PRT file in millisecond.
NB: Please rember to RENAME the LOG file before running

@author: apizz
"""

import pandas as pd
import numpy as np
import glob
import os


PATH_IN = "D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD"
SUBJ = ['sub-01']
SESS = [1]

for itersu, su in enumerate(SUBJ):
    for iterse in SESS:
        PATH_OUT = os.path.join(PATH_IN, su, 'Protocols','sess-0{}'.format(iterse),'Exp1_amb_MotQuart', 'Protocols')
        FILE_NAMES = glob.glob(os.fspath(os.path.join(PATH_IN, su, 'Protocols','sess-0{}'.format(iterse), 'Exp1_amb_MotQuart', 'Logging', '*.log')))
        N_RUNS = len(FILE_NAMES)

        for r in range(0, N_RUNS):

            # Extract run information
            basename = os.path.splitext(FILE_NAMES[r])
            corename = basename[0].split("\\")[-1]
            temp = corename.split("_")
            for it in temp:
                if (it == 'Run0{}'.format(r+1)):
                    info_run = it

            # // Read log file
            df = pd.read_table(FILE_NAMES[r], skiprows=18, delimiter = "\t")   # put back to skiprows=18
            df_array = df.values
            print("================================")
            print("Subject {}, {}".format(su, info_run))

            # Loop through list_keypress
            durations = []
            conditions = []
            on_off = []
            pre_conditions = []

            # Find part I need in the log file
            start_condition0 = df_array[:, -1] == 'StartOfCondition0'   # initial fixation
            start_condition1 = df_array[:, -1] == 'StartOfCondition1'   # baseline
            start_condition2 = df_array[:, -1] == 'StartOfCondition2'   # motion quartet
            start_condition3 = df_array[:, -1] == 'StartOfCondition3'   # final fixation
            qexit_condition = df_array[:, -1] == "User pressed quit"
            end_of_run = df_array[:, -1] == "EndOf{}".format(info_run)

            key1 = df_array[:, -1] == 'Keypress: 1'   # Horizontal
            key2 = df_array[:, -1] == 'Keypress: 2'   # Vertical

            idx = start_condition0 + start_condition1 + start_condition2 + start_condition3 + qexit_condition + key1 + key2 + end_of_run

            # Create a small version of df_array
            df_array_short = df_array[idx, : ]

            # Find perceptual periods
            exit_condition = np.where(df_array_short == "EndOf{}".format(info_run))  # Usually the exit condition is signed by the final Fixation
            myexit = exit_condition[0][-1]

            # Find Horizontal and Vertical periods
            i = 0
            while i < myexit + 1:
                if i > 0:
                    # Check pre-condition
                    if (df_array_short[i-1, -1] == "Keypress: 1") | (df_array_short[i-1, -1] == "Keypress: 2"):
                        pre_conditions.append("Task")
                    elif (df_array_short[i-1, -1] == "StartOfCondition0") | (df_array_short[i-1, -1] == "StartOfCondition3"):
                        pre_conditions.append("Fixation")
                    elif (df_array_short[i-1, -1] == "StartOfCondition1"):
                        pre_conditions.append("Baseline")

                if df_array_short[i, -1] == "Keypress: 1":   # // Horizontal
                    expect_cond = "Keypress: 2"

                    # Check end condition
                    if df_array_short[i+1, -1] == expect_cond:
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        durations.append(time)
                        on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+1, 0])])
                        conditions.append("Horizontal")

                    elif df_array_short[i+1, -1] == "StartOfCondition1":   # Edge case
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        durations.append(time)
                        on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+1, 0])])
                        conditions.append("Horizontal")

                elif (df_array_short[i, -1] == "Keypress: 2"):   # // Vertical
                    expect_cond = "Keypress: 1"

                    # Check end condition
                    if df_array_short[i+1, -1] == expect_cond:
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        durations.append(time)
                        on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+1, 0])])
                        conditions.append("Vertical")

                    elif df_array_short[i+1, -1] == "StartOfCondition1":   # Edge case
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        durations.append(time)
                        on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+1, 0])])
                        conditions.append("Vertical")

                elif (df_array_short[i, -1] == "StartOfCondition1"):   # // Baseline: can only be followed by condition2 or condition0

                    expect_cond1 = "StartOfCondition2"
                    expect_cond2 = "StartOfCondition0"
                    temp = df_array_short[i:, -1]
                    if ((df_array_short[i+1, -1] == expect_cond1) | (df_array_short[i+1, -1] == expect_cond2)):
                        time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                        durations.append(time)
                        on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+1, 0])])
                        conditions.append("Baseline")
                    
                    elif np.sum((temp == expect_cond1)) > 0:    
                        idx_next = np.where(temp == expect_cond1)[0][0]
                        time = float(df_array_short[i+idx_next, 0]) - float(df_array_short[i, 0])
                        durations.append(time)
                        on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+idx_next, 0])])
                        conditions.append("Baseline")
                    else:
                        idx_next = np.where(temp == expect_cond2)[0][0]
                        time = float(df_array_short[i+idx_next, 0]) - float(df_array_short[i, 0])
                        durations.append(time)
                        on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+idx_next, 0])])
                        conditions.append("Baseline")
                        
                elif (df_array_short[i, -1] == "StartOfCondition0"):   # // Initial Fixation
                    time = float(df_array_short[i+1, 0]) - float(df_array_short[i, 0])
                    durations.append(time)
                    on_off.append([float(df_array_short[i, 0]), float(df_array_short[i+1, 0])])
                    conditions.append("Fixation")


                i = i + 1

            # // Write protocol file
            prtName = os.path.join(PATH_OUT, 'Protocol_{}_{}_{}_{}.prt'.format(su, basename[0].split("\\")[5], basename[0].split("\\")[6], info_run))
            file = open(prtName, 'w')
            header = ['FileVersion: 2\n',
            'ResolutionOfTime: msec\n',
            'Experiment: Exp1_AmbiguousMotion\n',
            'BackgroundColor: 0 0 0\n',
            'TextColor: 255 255 202\n',
            'TimeCourseColor: 255 255 255\n',
            'TimeCourseThick: 3\n',
            'ReferenceFuncColor: 192 192 192\n',
            'ReferenceFuncThick: 2\n'
            'NrOfConditions: 4\n'
            ]

            file.writelines(header)

            # Write
            Labels = ['Fixation', 'Baseline', 'Horizontal', 'Vertical']
            Colors = ['Color: 64 64 64', 'Color: 150 150 150', 'Color: 255 0 0', 'Color: 0 255 0']
            for it, cond in enumerate(Labels):
                idx = np.asarray(conditions) == cond
                temp = np.int32(np.asarray(on_off)[idx, :] * 1000)
                n = np.shape(temp)[0]

                file.writelines(['\n{}\n{}\n'.format(cond, n)])

                for i in range(n):
                    file.writelines(['{} {}\n'.format(temp[i, 0], temp[i, 1])])

                file.writelines(['{}\n'.format(Colors[it])])
            file.close()

            # Write and save numpy array
            
            PRE_EVENT_INFO = dict()
            Cond2 = ['Horizontal', 'Vertical']
            for it, cond in enumerate(Cond2):
                temp = []
                idx = np.where(np.asarray(conditions) == cond)
                idx_pre = np.asarray(idx[0] - 1)
                if cond == 'Horizontal':
                    not_cond = 'Vertical'
                else:
                    not_cond = 'Horizontal'

                for i in range(0, len(idx_pre)):
                    if conditions[idx_pre[i]] == not_cond:
                        temp.append('task')
                    else:
                        temp.append('base')
                PRE_EVENT_INFO[cond] = temp
                outfile = os.path.join(PATH_OUT, 'Events_info_{}_{}_{}_{}.npy'.format(su, basename[0].split("\\")[5], basename[0].split("\\")[6], info_run))
                np.save(outfile, PRE_EVENT_INFO)

print("Success.")
