from psychopy import sound, visual, core, event
import glob
import random, os
import pandas as pd
from triggers import setParallelData

def check_quit():
    if event.getKeys(keyList=["escape"]):
            core.quit()

def play_and_trigger(stim, trigger):
    time1 = timer.getTime() #just for checking how long it takes
    setParallelData(trigger)
    time2 = timer.getTime()
    stim.play()
    time3 = timer.getTime()
    setParallelData(0)
    times = [time1, time2, time3]
    print(times)

win = visual.Window(
        size=[1920,1080],
        color="black",
        units="pix",
        screen=1,
        fullscr = True
    )

msg = visual.TextBox2(
        win,
        pos = (0,0),
        text = f'''
        Welcome to the experiment!

        You will soon be presented with a series of sounds.

        Press Q to begin

        '''
    )

stopwatch = core.Clock()

timestamp = data.getDateStr()

# data
#making sure there is a data folder
if not os.path.exists("data"):
    os.makedirs("data")

results = pd.DataFrame(
    columns = ["id", "gender", "age", "trail", "trigger"]
    )
filename = "data/experiment/{}_{}.csv".format(ID, timestamp)

fileList = glob.glob('sounds/*')
#randomising the list
fileList = random.shuffle(fileList)


#---The Experiment---
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

msg.draw()

win.flip()

while not event.getKeys(keyList=["q"]):
    pass
    check_quit()

win.flip()



for file in fileList:
    trigger = file[0:2]
    trail = fileList,index('file')
    win.callOnFlip(play_and_trigger, stim = sound.Sound(file, volume = 0.5), trigger = trigger) 
    #maybe we can just name them,starting from the trigger - 1_ for human and
    # 2_ for non-human or maybe 3_, 4_0 and so on for each different group of non-human sounds we decide to use
    win.flip()
    core.wait(5.0)
    results = results.append({
        "ID": ID, 
        "gender": gender,
        "age": age,
        "trail": trail,
        "trigger": trigger,
        },
        ignore_index = True
    )