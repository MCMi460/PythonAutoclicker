import tkinter as Tk
from pynput import keyboard
from pynput.mouse import Button, Controller
import threading
import time
import math

window = Tk.Tk()
window.title("Autoclicker v0.2")
window.geometry("800x400")
window.resizable(False,False)

mouse = Controller()
runclicker = False
holdclicker = False
window_closed = False
buttonvar = Button.left
click = True

frame = Tk.Frame(window, width=800, height=400)
frame.pack()

category = Tk.Label(frame,text="Click Interval")
category.config(font=("Helvetica",15))
category.place(x=0,y=20,width=100,height=20)

S = Tk.Text(frame,height=1,width=4)
S.insert("1.0", "0")
S.place(x=30,y=50)

seconds = Tk.Label(frame,text="Seconds")
seconds.config(font=("Helvetica",10))
seconds.place(x=60,y=50,width=50,height=20)

MS = Tk.Text(frame,height=1,width=4)
MS.insert("1.0", "1")
MS.place(x=120,y=50)

milseconds = Tk.Label(frame,text="Milliseconds")
milseconds.config(font=("Helvetica",10))
milseconds.place(x=160,y=50,width=60,height=20)

data = .001

def Update():
    global sdata
    global msdata
    temps = S.get("1.0",'end-1c')
    tempms = MS.get("1.0",'end-1c')
    try:
        sdata = int(temps)
        if len(str(sdata)) > 3:
            print("Please only type 3 digits for each interval.")
            return
    except:
        if temps == "":
            if tempms != "":
                sdata = 0
            else:
                print("You need something!")
                return
        else:
            print("Please only type integers for the seconds interval.")
            return
    try:
        msdata = int(tempms)
        if len(str(msdata)) > 3:
            print("Please only type 3 digits for each interval.")
            return
    except:
        if tempms == "":
            if temps != "":
                msdata = 0
            else:
                print("You need something!")
                return
        else:
            print("Please only type integers for the seconds interval.")
            return
    if msdata == 0 and sdata == 0:
        print("You need something!")
        msdata = 1
        return
    global data
    if msdata > 0 and sdata > 0:
        notice.config(text=f"{sdata}s, {msdata}ms")
        data = sdata + msdata / 1000
    elif msdata > 0:
        notice.config(text=f"{msdata}ms")
        data = msdata / 1000
    elif sdata > 0:
        notice.config(text=f"{sdata}s")
        data = sdata
    global buttonvar
    if buttontype.get() == "Left Click":
        buttonvar = Button.left
    elif buttontype.get() == "Right Click":
        buttonvar = Button.right
    global click
    if clickertype.get() == "Click":
        click = True
    elif clickertype.get() == "Hold":
        click = False
    print(f"Updated to {sdata}s, {msdata}ms, {buttontype.get()}, {clickertype.get()}")

setbutton = Tk.Button(frame,text="Update",font=("Helvetica",12),command=Update)
setbutton.place(x=220,y=50,width=60,height=20)

buttontype = Tk.StringVar(frame)
buttontype.set("Left Click")

buttonmenu = Tk.OptionMenu(frame, buttontype, "Left Click", "Right Click")
buttonmenu.config(font=("Helvetica",12))
buttonmenu.place(x=280,y=50,width=70,height=20)

clickertype = Tk.StringVar(frame)
clickertype.set("Click")

clickermenu = Tk.OptionMenu(frame, clickertype, "Click", "Hold")
clickermenu.config(font=("Helvetica",12))
clickermenu.place(x=350,y=50,width=70,height=20)

notice = Tk.Label(frame,text="Press F6 to start")
notice.config(font=("Helvetica",20))
notice.place(x=0,y=100,width=300,height=30)

title = Tk.Label(frame,text="Autoclicker v0.2")
title.config(font=("Helvetica",20))
title.place(x=250,y=5,width=300,height=20)

author = Tk.Label(frame,text="By Deltaion Lee")
author.config(font=("Helvetica",20))
author.place(x=250,y=350,width=300,height=50)
author.bind("<Button-1>", lambda e: print("https://mi460.dev/github"))

COMBINATIONS = [
    {keyboard.Key.f6}
]

current = set()

class Background(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            if runclicker:
                mouse.press(buttonvar)
                time.sleep(0.001)
                mouse.release(buttonvar)
                time.sleep(data)
            global holdclicker
            if holdclicker:
                mouse.press(buttonvar)
                for i in range(math.round(data)):
                    time.sleep(1)
                    if not holdclicker:
                        break
                mouse.release(buttonvar)
                holdclicker = False
            if window_closed:
                break

task = Background()
task.daemon = True
task.start()

def execute():
    global runclicker
    global holdclicker
    if click == True:
        if runclicker:
            runclicker = False
            holdclicker = False
        else:
            runclicker = True
            holdclicker = False
    elif click == False:
        if holdclicker:
            holdclicker = False
        else:
            holdclicker = True
        runclicker = False

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)

listener.start()
window.mainloop()
runclicker = False
holdclicker = False
window_closed = True
