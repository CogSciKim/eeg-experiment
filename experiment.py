from psychopy import sound, visual, core, event
import glob

def check_quit():
    if event.getKeys(keyList=["escape"]):
            core.quit()

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

fileList = glob.glob('sounds/*')

msg.draw()
win.flip()

while not event.getKeys(keyList=["q"]):
    pass
    check_quit()

win.flip()

for file in fileList:
    stim = sound.Sound(file,volume=0.5)
    stim.play()
    core.wait(3.0)