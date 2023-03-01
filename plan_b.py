from psychopy import sound, visual, core, event, data, gui
import glob
import random, os
import pandas as pd
from triggers import setParallelData

#dialogue box
Dialoguebox = gui.Dlg(title = "Information")
Dialoguebox.addField("Name:")
Dialoguebox.addField("Gender:", choices=["Female", "Male", "Other"])
Dialoguebox.addField("Age:")
Dialoguebox.show()

#saving the data from the dialogue box
if Dialoguebox.OK:
    id = Dialoguebox.data[0]
    gender = Dialoguebox.data[1]
    age = Dialoguebox.data[2]
elif Dialoguebox.Cancel:
    core.quit()

# data
#making sure there is a data folder
timestamp = data.getDateStr()

if not os.path.exists("data"):
    os.makedirs("data")

cols = ["id", "gender", "age", "trial", "trigger", "audio_name"]

results = pd.DataFrame(
    columns = cols
    )
filename = "data/{}_{}.csv".format(id, timestamp)

win = visual.Window(
        size=[1920,1080],
        color="white",
        units="pix",
        screen=1,
        fullscr = True
    )

def check_quit():
    if event.getKeys(keyList=["escape"]):
            core.quit()

#def play_and_trigger(stim, trigger):
#    setParallelData(0)
#    time1 = timer.getTime() #just for checking how long it takes
#    setParallelData(trigger)
#    time2 = timer.getTime()
#    stim.play()
#    time3 = timer.getTime()
    #setParallelData(0)
    #times = [time1, time2, time3]
    #print(times)
    
def fixation_cross():
    
    fixation = visual.TextStim(
        win, 
        text="+",
        color = 'black',
        height=100)
    
    fixation.draw()

msg = visual.TextBox2(
        win,
        pos = (0,0),
        font = 'Open Sans',
        color = 'black',
        text = '''
        Welcome to the experiment!

        You will soon be presented with a series of sounds.
        Please keep your eyes on the central cross.

        Press Q to begin

        '''
    )

final = visual.TextBox2(
        win,
        pos = (0,0),
        font = 'Open Sans',
        color = 'black',
        text = '''
        Thank you for your participation!

        Press Q to conclude the experiment
        '''
    )


#---The Experiment---
fileList = glob.glob('sounds/*')
#randomising the list
random.shuffle(fileList)
#fileList = fileList[0:8]
msg.draw()
win.flip()

while not event.getKeys(keyList=["q"]):
    pass
    check_quit()

timer = core.Clock()
fixation_cross()
win.flip()

PullTriggerDown = False 

for file in fileList:
    if event.getKeys(['escape']):
        results.to_csv(filename, index = False)
        core.quit()
    condition = int(file[7:8])
    if condition==1: 
        trigger = 11
    if condition==2: 
        trigger = 21
    trial = fileList.index(file)+1
    audio_name = file
    stim = sound.Sound(file, volume = 0.5)
    fixation_cross()
    win.callOnFlip(setParallelData, trigger) 
    PullTriggerDown = True 
    #time1 = timer.getTime()
    #print(time1)
    win.flip()
    stim.play()
    #time2 = timer.getTime()
    #print(time2) 
    core.wait(1.5)
    stim.stop(reset=False)
    core.wait(0.5)

    row = pd.Series({
        "id": id, 
        "gender": gender,
        "age": age,
        "trial": trial,
        "trigger": trigger,
        "audio_name": audio_name,
        })
    trialDf = pd.DataFrame(row,index=cols).T

    results = pd.concat([results,trialDf],
        ignore_index = True,
        axis=0
    )
    fixation_cross()
    if PullTriggerDown:
        win.callOnFlip(setParallelData, 0)
        PullTriggerDown = False 
    win.flip()


results.to_csv(filename,index=False)


final.draw()
win.flip()
event.waitKeys(keyList = ['escape', 'q'])
