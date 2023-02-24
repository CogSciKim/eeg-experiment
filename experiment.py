from psychopy import sound, visual, core, event, data, gui
import glob
import random, os
import pandas as pd
#from triggers import setParallelData

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

cols = ["id", "gender", "age", "trial", "trigger"]

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

def play_and_trigger(stim, trigger):
    time1 = timer.getTime() #just for checking how long it takes
    #setParallelData(trigger)
    time2 = timer.getTime()
    stim.play()
    time3 = timer.getTime()
    #setParallelData(0)
    times = [time1, time2, time3]
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
        font = 'Open Sans',
        text = '''
        Thank you for your participation!

        Press Q to conclude the experiment
        '''
    )


#---The Experiment---
fileList = glob.glob('sounds/*')
#randomising the list
random.shuffle(fileList)

msg.draw()
win.flip()

while not event.getKeys(keyList=["q"]):
    pass
    check_quit()

timer = core.Clock()
fixation_cross()
win.flip()

for file in fileList:
    trigger = int(file[7:8])
    trial = fileList.index(file)+1
    win.callOnFlip(play_and_trigger, stim = sound.Sound(file, volume = 0.5), trigger = trigger) 
    #maybe we can just name them,starting from the trigger - 1_ for human and
    # 2_ for non-human or maybe 3_, 4_0 and so on for each different group of non-human sounds we decide to use
    fixation_cross()
    win.flip()
    core.wait(1.2) # short trials for actual data
    row = pd.Series({
        "id": id, 
        "gender": gender,
        "age": age,
        "trial": trial,
        "trigger": trigger
        })
    trialDf = pd.DataFrame(row,index=cols).T

    results = pd.concat([results,trialDf],
        ignore_index = True,
        axis=0
    )


results.to_csv(filename,index=False)


final.draw()
win.flip()

while True:
    if event.getKeys(keyList=["q"]):
        break
