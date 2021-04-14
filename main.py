import tkinter as Tk
from pynput import keyboard
from pynput.mouse import Button, Controller
import threading
import time

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
times = 0

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
            notice.config(text=f"Please only type 3 digits for each interval.",font=("Helvetica",12))
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
            print("Please only type integers for the intervals.")
            notice.config(text=f"Please only type integers for the intervals.",font=("Helvetica",12))
            return
    try:
        msdata = int(tempms)
        if len(str(msdata)) > 3:
            print("Please only type 3 digits for each interval.")
            notice.config(text=f"Please only type 3 digits for each interval.",font=("Helvetica",12))
            return
    except:
        if tempms == "":
            if temps != "":
                msdata = 0
            else:
                print("You need something!")
                return
        else:
            print("Please only type integers for the intervals.")
            notice.config(text=f"Please only type integers for the intervals.",font=("Helvetica",12))
            return
    if msdata == 0 and sdata == 0:
        print("You need something!")
        msdata = 1
        return
    global buttonvar
    if buttontype.get() == "Left":
        buttonvar = Button.left
    elif buttontype.get() == "Right":
        buttonvar = Button.right
    global click
    if clickertype.get() == "Click":
        click = True
    elif clickertype.get() == "Hold":
        click = False
    global times
    times2 = "infinite"
    if rtype.get() == 1:
        times = 0
    elif rtype.get() == 2:
        try:
            times = int(rtimes.get("1.0",'end-1c'))
            if len(str(times)) > 3:
                print("Please only type 3 digits for the repeat value.")
                notice.config(text=f"Please only type 3 digits for the repeat value.",font=("Helvetica",12))
                times = 0
                return
            times2 = f"{times}"
        except:
            print("Please enter an integer for the repeat value.")
            notice.config(text=f"Please enter an integer for the repeat value.",font=("Helvetica",12))
            times = 0
            return
    global data
    if msdata > 0 and sdata > 0:
        notice.config(text=f"{buttontype.get()} {clickertype.get()} {times2} times, {sdata}s, {msdata}ms",font=("Helvetica",20))
        data = sdata + msdata / 1000
    elif msdata > 0:
        notice.config(text=f"{buttontype.get()} {clickertype.get()} {times2} times, {msdata}ms",font=("Helvetica",20))
        data = msdata / 1000
    elif sdata > 0:
        notice.config(text=f"{buttontype.get()} {clickertype.get()} {times2} times, {sdata}s",font=("Helvetica",20))
        data = sdata
    print(f"Updated to {sdata}s, {msdata}ms, {buttontype.get()} {clickertype.get()} {times2} times")

setbutton = Tk.Button(frame,text="Update",font=("Helvetica",12),command=Update)
setbutton.place(x=220,y=50,width=60,height=20)

buttontype = Tk.StringVar(frame)
buttontype.set("Left")

buttonmenu = Tk.OptionMenu(frame, buttontype, "Left", "Right")
buttonmenu.config(font=("Helvetica",12))
buttonmenu.place(x=280,y=50,width=55,height=20)

clickertype = Tk.StringVar(frame)
clickertype.set("Click")

clickermenu = Tk.OptionMenu(frame, clickertype, "Click", "Hold")
clickermenu.config(font=("Helvetica",12))
clickermenu.place(x=335,y=50,width=70,height=20)

rtype = Tk.IntVar(frame)
rtype.set(1)

repeatmenu = Tk.Radiobutton(frame, text='Repeat until stopped',variable=rtype,value=1)
repeatmenu.config(font=("Helvetica",12))
repeatmenu.place(x=500,y=50,width=130,height=20)

repeatmenu2 = Tk.Radiobutton(frame, text='Repeat',variable=rtype,value=2)
repeatmenu2.config(font=("Helvetica",12))
repeatmenu2.place(x=500,y=80,width=70,height=20)

rtimes = Tk.Text(frame,height=1,width=3)
rtimes.insert("1.0", "10")
rtimes.place(x=563,y=81)

word = Tk.Label(frame,text="times")
word.config(font=("Helvetica",12))
word.place(x=590,y=80,width=30,height=20)

notice = Tk.Label(frame,text="Press F6 to start")
notice.config(font=("Helvetica",20))
notice.place(x=225,y=350,width=350,height=30)

title = Tk.Label(frame,text="Autoclicker v0.2")
title.config(font=("Helvetica",20))
title.place(x=250,y=5,width=300,height=20)

author = Tk.Label(frame,text="By Deltaion Lee")
author.config(font=("Helvetica",12))
author.place(x=340,y=25,width=120,height=20)
author.bind("<Button-1>", lambda e: print("https://mi460.dev/github"))

COMBINATIONS = [
    {keyboard.Key.f6}
]

current = set()

class Background(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            if window_closed:
                break
            global runclicker
            global holdclicker
            if times == 0:
                if runclicker:
                    mouse.press(buttonvar)
                    time.sleep(0.001)
                    mouse.release(buttonvar)
                    time.sleep(data)
                if holdclicker:
                    mouse.press(buttonvar)
                    for i in range(round(data)):
                        time.sleep(1)
                        if not holdclicker:
                            break
                    mouse.release(buttonvar)
                    time.sleep(0.5)
            else:
                if runclicker:
                    for i in range(times):
                        if not runclicker:
                            break
                        mouse.press(buttonvar)
                        time.sleep(0.001)
                        mouse.release(buttonvar)
                        time.sleep(data)
                    runclicker = False
                if holdclicker:
                    for i in range(times):
                        if not holdclicker:
                            break
                        mouse.press(buttonvar)
                        for i in range(round(data)):
                            time.sleep(1)
                            if not holdclicker:
                                break
                        mouse.release(buttonvar)
                        time.sleep(0.5)
                    holdclicker = False

task = Background()
task.daemon = True
task.start()

def execute():
    global runclicker
    global holdclicker
    if click == True:
        if runclicker:
            runclicker = False
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
