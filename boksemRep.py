#script tested in Python 3.10.0 wwith PsychoPy 2024.1.4
from psychopy import visual, core,data,event,gui
import math, random

#function to send trigger signal to EEG system
#NOTE: need to adjust this function to your EEG system; definitely check if the trigger is sent correctly before starting data collection
#contact Jakob Kaiser if you need help with this (jkbkaiser@googlemail.com)
#NOTE: trigger in scipt is an integer value 0-255 => adjust to your EEG system
def sendTrigger(trigger):
    print('Trigger %i' % trigger)
    #replace this with your system-specific trigger sending function


#number of screens => adjust to your setup depending on how many screens you have connected
screenNumber = 2


expInfo = {'pnum':0, 'age':0, 'gender':'n', 'practice':True}
gender=-1

dlg = gui.DlgFromDict(expInfo, title='Please type in participant information', sortKeys=False, labels={'pnum':'Participant Number', 'age':'Age', 'gender':'Gender ([m]ale/[f]emale/[d]ivers/[n]o response)', 'practice':'YES = Practice Mode during EEG Prep ||| NO = Main Experiment'})
practice = expInfo['practice']
if expInfo['gender']=='m' or expInfo['gender']=='M': gender=0
if expInfo['gender']=='f' or expInfo['gender']=='F': gender=1
if expInfo['gender']=='d' or expInfo['gender']=='D': gender=2
if expInfo['gender']=='n' or expInfo['gender']=='N': gender=3
if not(isinstance(expInfo['pnum'],int)) or not(isinstance(expInfo['age'],int)) or gender==-1:
    print('Wrong format in participant information - please restart and try again.')
    core.quit() 

if expInfo['pnum'] == 0 or expInfo['age'] == 0:
    print('Please specify participate ID an age.')
    core.quit()




pnum = expInfo['pnum']
expInfo['dateStr'] = data.getDateStr()  # add the current time
if practice:
    strAdd = 'PRACTICE'
else:
    strAdd = 'MAIN'
fileName = 'simonExp_' + strAdd + '_p' + str(pnum) + '_' + expInfo['dateStr']
dataFile = open (fileName + '.csv', 'w')
#defining header => make sure this matches order of actual data logged on each trial
dataFile.write('pnum,age,gender,practice,phase,timerPhase,tnum,stimPos,stimType,congruent,firstResp,firstRT,postResp,postRT,frameRate,ITI,trigger,winszX,winszY\n')

#defining experiment window
mywin = visual.Window(fullscr=True, monitor="testMonitor", screen=screenNumber, units="deg", color=(-1, -1, -1), checkTiming=True)
screenX = mywin.size[0]
screenY = mywin.size[1]
frameDur = mywin.monitorFramePeriod
#Load the  fixation cross picture
# fixation = visual.TextBox2(win=mywin, text="*", color=(1,1,1),size=[0.1, 0.1], pos=[0,0],units="deg", alignment="center",font="Arial")

# Load the picture
fixation = visual.ImageStim(win=mywin, image="fixation.png", size=[0.5, 0.5], pos=[0,0], units="deg")

#symbols for cue arrows
arrowLeft = visual.ImageStim(win=mywin, image="cueLeft.png", size=[0.5, 0.5], pos=[0,0.6], units="deg")
arrowRight = visual.ImageStim(win=mywin, image="cueRight.png", size=[0.5, 0.5], pos=[0,0.6], units="deg")
arrows = [arrowLeft,arrowRight]

#symbols for action signals
leftActLeftPos =  visual.ImageStim(win=mywin, image="stimLeft.png", size=[0.5, 0.5], pos=[-2.2, 0], units="deg")
leftActRightPos = visual.ImageStim(win=mywin, image="stimLeft.png", size=[0.5, 0.5], pos=[2.2, 0], units="deg")
rightActLeftPos = visual.ImageStim(win=mywin, image="stimRight.png", size=[0.5, 0.5], pos=[-2.2, 0], units="deg")
rightActRightPos = visual.ImageStim(win=mywin, image="stimRight.png", size=[0.5, 0.5], pos=[2.2, 0], units="deg")

leftAct = [leftActLeftPos,leftActRightPos]
rightAct = [rightActLeftPos,rightActRightPos]
actSignal = [leftAct,rightAct]


#starting instructions for EEG experiment
instrtxt1 = ("****" + strAdd + " PHASE****\n" +
"Thank you for taking part in this experiment.\n" +
"This experiment will last a while. The exact duration will be determined by the experiment software during runtime.\n" +
"In any case, this experiment will be finished at 6 pm at the latest.\n" +
"For this experiment it is important that you cannot use your phone or watch during the procedure.\n" +
"If you have not yet done so, we would ask you to give your phone and watch to the experimenter for safekeeping.\n" +
"For the EEG measurement to work, please try to avoid any movements except the key presses necessary for the task.\n" +
"Please let the experimenter know if you have any questions.\n" +
"The next screen will show you the task instructions.\n" +
"When you are ready to read the task instructions, press ENTER.")

#instructions for Simon task
instrtxt2 = ("****" + strAdd + " PHASE****\n" +
"In this task, you will see a star (*) as a fixation symbol in the middle of the screen. Try to always keep your eyes on the fixation symbol.\n" +
"Occasionally, either the letter H or the letter S will appear left or right to the fixation symbol. Depending on the letter you have to press a key as quickly as possible.\n" +
"If the letter is an H, press the LEFT-arrow key with your LEFT index finger.\n" +
"If the letter is an S, press the RIGHT-arrow key with your RIGHT index finger.\n" +
"It is important that you always try to respond both CORRECTLY AND as QUICKLY as possible.\n" +
"Please let the experimenter know if you have any questions about this task.\n" +
"When you are ready to start, press ENTER to begin.")

#instructions for the second phase of the experiment
instrtxt3 = ("" +
"Now, the same task as before will continue. However, there is one important change.\n" +
"From now on, your response accuracy and response speed will be recorded for comparison.\n" +
"After data collection, we will compare your ACCURACY and RESPONSE SPEED from this point on with the performance of all other participants.\n" +
"At the end of data collection, the 10 participants with the most accurate and fastest performance will receive an extra 25 Euros payment.\n" +
"Therefore, try your best to be as accurate and fast as possible!\n" +
"Press ENTER to continue with the task.\n")

instructions = []
instructions.append(visual.TextBox2(win=mywin, text=instrtxt1, color=(1,1,1),pos=[0,0],units="deg",size=[22,None]))
instructions.append(visual.TextBox2(win=mywin, text=instrtxt2, color=(1,1,1),pos=[0,0],units="deg",size=[22,None]))
instructions.append(visual.TextBox2(win=mywin, text=instrtxt3, color=(1,1,1),pos=[0,0],units="deg",size=[22,None]))
if practice:
    num_phases = 1
    duration_phases = [0.05*60] # durations in seconds; practice phase in original experiment during EEG preparation consists of 15 min
else:
    num_phases = 2
    duration_phases = [0.05*60, 0.01*60] # durations in seconds; original experiment consists of first phase=120 min and second phase=20 min
#determining timings of individual trial phases
time_cue = 0.15
time_action = 1.2
time_after = 0.5
time_itiLow = 0.4
time_itiHigh = 0.6

flips_cue = math.ceil(time_cue/frameDur)
flips_action = math.ceil(time_action/frameDur)
flips_after = math.ceil(time_after/frameDur)
flips_iti = [math.ceil(time_itiLow/frameDur), math.ceil(time_itiHigh/frameDur)]

instructions[0].draw()
mywin.flip()
allKeys=event.waitKeys(keyList = "return")
instructions[1].draw()
mywin.flip()
allKeys=event.waitKeys(keyList = "return")
thisPhase = 1
trialsLeft = 0
timerPhase = core.Clock()
timerRT = core.Clock()
while thisPhase <= num_phases:
#if the timer for one phase (=20 minutes) is run down the next phase starts
    if timerPhase.getTime() >= duration_phases[thisPhase-1]:
        thisPhase += 1
        if thisPhase == num_phases+1:
            break
        instructions[thisPhase].draw()
        mywin.flip()
        allKeys=event.waitKeys(keyList = "return")
        timerPhase.reset()
        
    
    if trialsLeft == 0:
        #create a new list of trials
        trialList = []
        for stimPos in [0,1]:
            for response in [0,1]:
                for congruent in [0,0,1,1,1,1,1,1,1,1]:
                    # append a python 'dictionary' to the list
                    trialList.append({'stimPos': stimPos, 'stimType': response, 'congruent': congruent})
        trialsLeft = len(trialList)
        trials = data.TrialHandler(trialList, 1, method="random",
                           extraInfo={'participant': str(pnum), 'session': practice})
    
    thisTrial = trials.next()
    msg = 'Phase %i: timer %d; trial %i out of %i had position %i in the list (stimPos=%i, response=%i, congruent=%i)'
    print(msg % (thisPhase, timerPhase.getTime(), trials.thisN, trialsLeft, trials.thisIndex, thisTrial['stimPos'], thisTrial['stimType'], thisTrial['congruent']))
    triggerID = thisTrial['congruent'] + 3*thisTrial['stimPos'] + 10*thisTrial['stimType'] + 100*thisPhase

    if thisTrial['congruent']==1:
        arrowNum = thisTrial['stimPos']
    else:
        arrowNum = (thisTrial['stimPos']+1) % 2
    
    
    #ITI
    flips_thisITI = random.randint(flips_iti[0], flips_iti[1])
    for frameN in range(flips_thisITI):
        # Present the picture on the window
        fixation.draw()
        mywin.flip()
    
    
    for frameN in range(flips_cue):
        if frameN == 0:
            #sending trigger to EEG
            sendTrigger(triggerID)
        if frameN == flips_cue-1:
            #turn off trigger by sending 0
            sendTrigger(0)

        fixation.draw()
        arrows[arrowNum].draw()
        mywin.flip()
    
    frameN = 0
    firstResp=-1
    firstRT=-1
    respCorrect=0
    timerRT.reset()
    while firstResp == -1 and frameN <= flips_action:
        fixation.draw()
        actSignal[thisTrial['stimType']][thisTrial['stimPos']].draw()
        mywin.flip()
        allKeys=event.getKeys(keyList = ['left','right'],timeStamped=timerRT)
        for thisKey in allKeys:
            if thisKey[0]=='left': 
                firstResp = 0
                firstRT = thisKey[1]
                print(thisKey[0])
            if thisKey[0]=='right': 
                firstResp = 1
                firstRT = thisKey[1]
                print(thisKey[0])
        frameN += 1
    #print(timerRT.getTime())
    
    frameN = 0
    postResp=-1
    postRT=-1
    while  frameN <= flips_after:
        fixation.draw()
        mywin.flip()
        allKeys=event.getKeys(keyList = ['left','right'],timeStamped=timerRT)
        for thisKey in allKeys:
            if thisKey[0]=='left': 
                postResp = 0
                postRT = thisKey[1]
                print(thisKey[0])
            if thisKey[0]=='right': 
                postResp = 1
                postRT = thisKey[1]
                print(thisKey[0])
        frameN += 1
    trialsLeft -= 1
    dataFile.write('%i,%i,%i,%i,%i,%.3f,%i,%i,%i,%i,%i,%.5f,%i,%.5f,%.5f,%i,%i,%i,%i\n' %(pnum,expInfo['age'],gender,practice,thisPhase,timerPhase.getTime(),trials.thisN,thisTrial['stimPos'], thisTrial['stimType'], thisTrial['congruent'], firstResp, firstRT,postResp, postRT, frameDur, flips_thisITI, triggerID, screenX, screenY))
dataFile.close()

 