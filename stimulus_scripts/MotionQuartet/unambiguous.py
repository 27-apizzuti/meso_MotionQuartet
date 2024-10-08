"""
It presents physical motion quartet stimulus.
Block design:
Motion condition: (5 triggers (10s) horizontal motion, 5 triggers vertical motion) x 4 times; followed by control condition: Flickering quartet (8 triggers)
There are 6 blocks in total.
The stimulus begins and ends with a fixation condition of 20s.

Total triggers: 308
Total time: (308)*2s=[10min20s]

Psychopy3 (v2020.2.4)
Based on https://github.com/MSchnei/motion_quartet_scripts (@author: Marian.Schneider)

@author: Alessandra Pizzuti
"""
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, event, core, monitors, logging, gui, data, misc
from itertools import cycle
import numpy as np
import os

# # ------------------------------------------------------------------------------
# from psychopy import visual, event, core, gui
# from psychopy.hardware.emulator import launchScan
#
# # settings for launchScan:
# MR_settings = {
#     'TR': 0.5,         # duration (sec) per whole-brain volume
#     'volumes': 523,  # number of whole-brain 3D volumes per scanning run
#     'sync': 5,       # character to use as the sync timing event; assumed to come at start of a volume
#     'skip': 0,       # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
#     'sound': False   # in test mode: play a tone as a reminder of scanner noise
#     }
# # infoDlg = gui.DlgFromDict(MR_settings, title='fMRI parameters', order=['TR', 'volumes'])
# # if not infoDlg.OK:
# #     core.quit()
# win = visual.Window(fullscr=False)
# # output = u'vol    onset key\n'
# # for i in range(-1 * MR_settings['skip'], 0):
# #     output += u'%d prescan skip (no sync)\n' % i
# # --------------------------------------------------------------------------------


# %% SET PARAMS
# specify vertical distance for this participant
VertiDist = 3.8
# specificy background color
backColor = [-0.5, -0.5, -0.5]  # from -1 (black) to 1 (white)
# specificy square color
squareColor = np.multiply(backColor, -1)  # from -1 (black) to 1 (white)

# %% SAVING and LOGGING
# Store info about experiment and experimental run
expName = 'Exp1_Phys_MotQuart'  # set experiment name here
expInfo = {
    u'run': u'0',
    u'participant': u'sub-0',
    }
# Create GUI at the beginning of exp to get more expInfo
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# get the path that this script is in and change dir to it
_thisDir = os.path.dirname(os.path.abspath(__file__))  # get current path
os.chdir(_thisDir)  # change directory to this path

# Name and create specific subject folder
subjFolderName = '%s_SubjData' % (expInfo['participant'])
if not os.path.isdir(subjFolderName):
    os.makedirs(subjFolderName)
# Name and create data folder for the experiment
dataFolderName = subjFolderName + os.path.sep + '%s' % (expInfo['expName'])
if not os.path.isdir(dataFolderName):
    os.makedirs(dataFolderName)
# Name and create specific folder for logging results
logFolderName = dataFolderName + os.path.sep + 'Logging'
if not os.path.isdir(logFolderName):
    os.makedirs(logFolderName)
logFileName = logFolderName + os.path.sep + '%s_%s_Run%s_%s' % (
    expInfo['participant'], expInfo['expName'], expInfo['run'],
    expInfo['date'])
# Name and create specific folder for protocol files
prtFolderName = dataFolderName + os.path.sep + 'Protocols'
if not os.path.isdir(prtFolderName):
    os.makedirs(prtFolderName)

# save a log file and set level for msg to be received
logFile = logging.LogFile(logFileName+'.log', level=logging.INFO)
logging.console.setLevel(logging.WARNING)  # set console to receive warnings

# %% MONITOR AND WINDOW
# set monitor information:
distanceMon = 99  # [58] in psychoph lab [99] in scanner
widthMon = 30  # [53] in psychoph lab [30] in scanner
PixW = 1920.0  # [1920.0] in psychopy lab [1920.0] in scanner
PixH = 1200.0  # [1080.0] in psychoph lab [1200.0] in psychoph lab

moni = monitors.Monitor('testMonitor', width=widthMon, distance=distanceMon)
moni.setSizePix([PixW, PixH])  # [1920.0, 1080.0] in psychoph lab

# log monitor info
logFile.write('MonitorDistance=' + str(distanceMon) + 'cm' + '\n')
logFile.write('MonitorWidth=' + str(widthMon) + 'cm' + '\n')
logFile.write('PixelWidth=' + str(PixW) + '\n')
logFile.write('PixelHeight=' + str(PixH) + '\n')

# set screen:
myWin = visual.Window(size=(PixW, PixH),
                      screen = 0,
                      winType='pyglet',  # winType : None, ‘pyglet’, ‘pygame’
                      allowGUI=False,
                      allowStencil=False,
                      fullscr=True,  # for psychoph lab: fullscr = True
                      monitor=moni,
                      color=backColor,
                      colorSpace='rgb',
                      units='deg',
                      blendMode='avg',
                      )


# %% BLOCKS
# set number of repetitions for each condition
# fixation = 0; horiM = 1; vertiM = 2; flickerSl = 3
NumOf12PerBlock = 8  # number of blocks (hor + ver + flick)
NumQuartets = 6
Cond_elem = np.tile([1, 2], int(NumOf12PerBlock/2))
Conditions = np.tile(Cond_elem, NumQuartets)
pos_baseline = np.arange(NumOf12PerBlock, NumOf12PerBlock*(NumQuartets+1), NumOf12PerBlock)
Conditions = np.insert(Conditions, pos_baseline, [3])   # Insert baseline condition
Conditions = np.hstack(([0], Conditions, [0]))          # Add fixation condition
Conditions = Conditions.astype(np.int32)
logFile.write('Conditions=' + str(Conditions) + '\n')

print(Conditions)

# %% BLOCK DURATIONS [Triggers]
# set durations of conditions and baseline
TR = 1.6   # seconds
MotionDur = np.int(np.ceil(9.6 / TR))     # Vertical or Horizontal motion
BaseDur = np.int(16 / TR)        # 4 sqares flickering
Fixation = np.int(16 / TR)      # Fixation (beginning and end)
print(MotionDur)
# NOTE: Fixation at the beginning and at the end lasts both for 10 triggers.

Durations = np.ones(len(Conditions), dtype=np.int)*MotionDur
Durations[Conditions == 3] = BaseDur
Durations[Conditions == 0] = Fixation  # Dur fixation

Durations = Durations.astype(int)
logFile.write('Durations (Triggers) =' + str(Durations) + '\n')

# create array to log key pressed events
KeyPressedArray = np.array(['KeyPressed', 't'])

# %% STIMULI
# INITIALISE SOME STIMULI
SquareSize = 1.0  # 1.1 #1.8
SquareDur = 0.15  # in seconds # 9 frames
BlankDur = 0.067  # in seconds # 5 frames
HoriDist = 3.0

logFile.write('SquareSize=' + str(SquareSize) + '\n')
logFile.write('SquareDur=' + str(SquareDur) + '\n')
logFile.write('BlankDur=' + str(BlankDur) + '\n')

message = visual.TextStim(myWin,
                          text='Condition',
                          pos=(-16, -8)
                          )

dotFix = visual.Circle(myWin,
                       autoLog=False,
                       name='dotFix',
                       units='pix',
                       radius=10,
                       fillColor='red',
                       lineColor='red'
                       )

Square = visual.GratingStim(myWin,
                            autoLog=False,
                            name='Square',
                            tex=None,
                            units='deg',
                            size=(SquareSize, SquareSize),
                            color= squareColor,
                            )

triggerText = visual.TextStim(
    win=myWin,
    color='white',
    height=0.5,
    text='Experiment will start soon. Waiting for scanner'
    )


# %% TIME AND TIMING PARAMeTERS
# parameters
totalTrigger = np.sum(Durations)   # 308
print(totalTrigger)
# get screen refresh rate
refr_rate = myWin.getActualFrameRate()  # get screen refresh rate
if refr_rate is not None:
    frameDur = 1.0/round(refr_rate)
else:
    frameDur = 1.0/60.0  # couldn't get a reliable measure so guess
logFile.write('RefreshRate=' + str(refr_rate) + '\n')
logFile.write('FrameDuration=' + str(frameDur) + '\n')

# define clock
clock = core.Clock()
logging.setDefaultClock(clock)

# %% FUNCTIONS
# create necessary functions for quartet and flicker
NumSquareFrames = int(round(SquareDur/frameDur))  # num of square frames
NumBlankFrames = int(round(BlankDur/frameDur))  # num of blank frames
TravelTime = 2*NumSquareFrames+2*NumBlankFrames
TravelTimeArray = np.arange(TravelTime+1)/TravelTime
HoriTimeCycle = cycle(TravelTimeArray)  # iterate through the TravelTimeArray
VertiTimeCycle = cycle(TravelTimeArray)  # iterate through the TravelTimeArray

def HMotion_update(Hori, Verti):
    x = next(HoriTimeCycle)  # pick next element when cycling TravelTimeArray
    mHori = np.cos((2*np.pi)*x)*Hori
    Square.setPos((mHori, Verti))  # square northeast
    Square.draw()
    Square.setPos((-mHori, -Verti))  # square southwest
    Square.draw()
    dotFix.draw()
    myWin.flip()
    return mHori

def VMotion_update(Hori, Verti):
    x = next(VertiTimeCycle)
    mVerti = np.cos((2*np.pi)*x)*Verti
    Square.setPos((-Hori, mVerti))  # square northwest
    Square.draw()
    Square.setPos((Hori, -mVerti))  # square southeast
    Square.draw()
    dotFix.draw()
    myWin.flip()
    return mVerti

def flickerSl(Hori, Verti):
    NumSquareFrames = int(round(SquareDur/frameDur))
    NumBlankFrames = 2*int(round(BlankDur/frameDur)) + NumSquareFrames
    for frameN in range(NumSquareFrames):
        Square.setPos((-Hori, Verti))
        Square.draw()
        Square.setPos((Hori, -Verti))
        Square.draw()
        Square.setPos((Hori, Verti))
        Square.draw()
        Square.setPos((-Hori, -Verti))
        Square.draw()
        dotFix.draw()
        myWin.flip()
    for frameN in range(NumBlankFrames):
        dotFix.draw()
        myWin.flip()

# %% RENDER_LOOP
# give the system time to settle
core.wait(1)

# wait for scanner trigger
triggerText.draw()
myWin.flip()
# # --------------------------------------------
# launch: operator selects Scan or Test (emulate); see API documentation
# vol = launchScan(win, MR_settings, globalClock=clock, mode='Scan')
# #----------------------------------------------
event.waitKeys(keyList=['5'], timeStamped=False)

# Create Counters
i = 0           # counter for blocks
trigCount = 1   # counter triggers

# reset clocks
# clock.reset()
print(totalTrigger)
logging.data('StartOfRun' + str(expInfo['run']))

while trigCount < totalTrigger:    # 308

    logging.data('StartOfCondition'+ str(Conditions[i]))

    while trigCount < np.sum(Durations[0:i+1]):
        t = clock.getTime()

        if Conditions[i] == 0:
            dotFix.draw()
            myWin.flip()
        elif Conditions[i] == 1:
            mHori = HMotion_update(HoriDist, VertiDist)
        elif Conditions[i] == 2:
            mVerti = VMotion_update(HoriDist, VertiDist)
        elif Conditions[i] == 3:
            flickerSl(HoriDist, VertiDist)

        for key in event.getKeys():
                if key in ['escape', 'q']:
                    logging.data(msg='User pressed quit')
                    myWin.close()
                    core.quit()
                elif key in ['1', 'num_1']:
                    t = clock.getTime()
                    KeyPressed = '1'
                    KeyPressedNew = np.array([KeyPressed, t])
                    KeyPressedArray = np.vstack((KeyPressedArray,
                                                 KeyPressedNew))
                    logging.data(msg='Key1 pressed')
                elif key in ['2', 'num_2']:
                    t = clock.getTime()
                    KeyPressed = '2'
                    KeyPressedNew = np.array([KeyPressed, t])
                    KeyPressedArray = np.vstack((KeyPressedArray,
                                                 KeyPressedNew))
                    logging.data(msg='Key2 pressed')
                elif key in ['5']:
                    t = clock.getTime()
                    trigCount = trigCount + 1
                    logging.data(msg='Scanner trigger %i' % (trigCount))

    i = i+1
    print('Block counter: %i' % i)

logging.data('EndOfRun' + str(expInfo['run']) + '\n')

# %% CLOSE DISPLAY
myWin.close()

# %% SAVE DATA
try:
    # calculate speed [degrees per frame]
    HoriSpeed = (HoriDist*4)/TravelTime
    VertiSpeed = (VertiDist*4)/TravelTime
    logFile.write('HoriSpeed=' + str(HoriSpeed) + '\n')
    logFile.write('VertiSpeed=' + str(VertiSpeed) + '\n')
    logFile.write('HoriDist=' + str(HoriDist) + '\n')
    logFile.write('VertiDist=' + str(VertiDist) + '\n')
    print('horizontalDistance: %f' % HoriDist)
    print('verticalDistance: %f' % VertiDist)
    print(KeyPressedArray)

except:
    print('(Key variables could not be saved.)')

# create prt files for BV
try:
    os.chdir(prtFolderName)
    # Set Conditions Names
    CondNames = ['Fixation',
                 'Flicker',
                 'Horizontal',
                 'Vertical',
                 ]

    # Number code the conditions, i.e. Fixation = -1, Static = 0, etc.
    from collections import OrderedDict
    stimTypeDict = OrderedDict()
    stimTypeDict[CondNames[0]] = [0]
    stimTypeDict[CondNames[1]] = [3]
    stimTypeDict[CondNames[2]] = [1]
    stimTypeDict[CondNames[3]] = [2]

    # Color code the conditions
    colourTypeDict = {
        CondNames[0]: '64 64 64',
        CondNames[1]: '150 150 150',
        CondNames[2]: '255 0 0',
        CondNames[3]: '0 255 0',
        }

    # Defining a function will reduce the code length significantly.
    def idxAppend(iteration, enumeration, dictName, outDict):
        if int(enumeration) in range(stimTypeDict[dictName][0],
                                     stimTypeDict[dictName][-1]+1
                                     ):
            outDict = outDict.setdefault(dictName, [])
            outDict.append(iteration)

    # Reorganization of the protocol array (finding and saving the indices)
    outIdxDict = {}  # an empty dictionary

    # Please take a deeper breath.
    for i, j in enumerate(Conditions):
        for k in stimTypeDict:  # iterate through each key in dict
            idxAppend(i, j, k, outIdxDict)

    print(outIdxDict)

    # Creation of the Brainvoyager .prt custom text file
    prtName = '%s_%s_Run%s_%s.prt' % (expInfo['participant'],
                                      expInfo['expName'], expInfo['run'],
                                      expInfo['date'])

    file = open(prtName, 'w')
    header = ['ResolutionOfTime: Volumes\n',
              'Experiment: %s\n' % expName,
              'BackgroundColor: 0 0 0\n',
              'TextColor: 255 255 202\n',
              'TimeCourseColor: 255 255 255\n',
              'TimeCourseThick: 3\n',
              'ReferenceFuncColor: 192 192 192\n',
              'ReferenceFuncThick: 2\n'
              'NrOfConditions: %s\n' % str(len(stimTypeDict))
              ]

    file.writelines(header)

    # Conditions/predictors
    for i in stimTypeDict:  # iterate through each key in stim. type dict
        h = i

        # Write the condition/predictor name and put the Nr. of repetitions
        file.writelines(['\n',
                         i+'\n',
                         str(len(outIdxDict[i]))
                         ])

        # iterate through each element, define onset and end of each condition
        for j in outIdxDict[i]:
            onset = int(sum(Durations[0:j+1]) - Durations[j] + 1)
            file.write('\n')
            file.write(str(onset))
            file.write(' ')
            file.write(str(onset + Durations[j]-1))
        # contiditon color
        file.write('\nColor: %s\n' % colourTypeDict[h])

    file.close()
    print('PRT files saved as: ' + prtFolderName + '//' + prtName)
    os.chdir(_thisDir)
except:
    print('(PRT files could not be created.)')

# %% FINISH
core.quit()
