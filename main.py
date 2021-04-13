import tkinter as Tk
from pynput import keyboard
from pynput.mouse import Button, Controller
import threading
import time

window = Tk.Tk()
window.title("Autoclicker v0.1")
window.geometry("800x400")
window.resizable(False,False)

mouse = Controller()
runclicker = False

my_frame = Tk.Frame(window, width=800, height=400)
my_frame.pack()

S = Tk.Text(my_frame,height=1,width=4)
S.insert("1.0", "0")
S.place(x=30,y=50)

seconds = Tk.Label(my_frame,text="Seconds")
seconds.config(font=("Helvetica",10))
seconds.place(x=60,y=50,width=50,height=20)

MS = Tk.Text(my_frame,height=1,width=4)
MS.insert("1.0", "1")
MS.place(x=120,y=50)

milseconds = Tk.Label(my_frame,text="Milliseconds")
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
        notice.config(text=f"S: {sdata}, MS: {msdata}")
        data = sdata + msdata / 1000
    elif msdata > 0:
        notice.config(text=f"MS: {msdata}")
        data = msdata / 1000
    elif sdata > 0:
        notice.config(text=f"S: {sdata}")
        data = sdata
    print("Updated")

setbutton = Tk.Button(my_frame,text="Update",font=("Helvetica",12),command=Update)
setbutton.place(x=220,y=50,width=60,height=20)

notice = Tk.Label(my_frame,text="Press F6 to start")
notice.config(font=("Helvetica",20))
notice.place(x=0,y=100,width=300,height=30)

title = Tk.Label(my_frame,text="Autoclicker v0.1")
title.config(font=("Helvetica",20))
title.place(x=250,y=5,width=300,height=20)

author = Tk.Label(my_frame,text="By Deltaion Lee")
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
                mouse.press(Button.left)
                time.sleep(0.001)
                mouse.release(Button.left)
                time.sleep(data)

task = Background()
task.start()

def execute():
    global runclicker
    if runclicker:
        runclicker = False
    else:
        runclicker = True

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
