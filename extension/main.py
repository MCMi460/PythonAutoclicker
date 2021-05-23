import tkinter as Tk
from pynput import keyboard
from pynput.mouse import Button, Controller, Listener
import threading
import time
import random

version = 0.1

window = Tk.Tk()
window.title(f"Hypixel Autoclicker v{version}")
window.geometry("800x400")
window.resizable(False,False)

mouse = Controller()
active = False
window_closed = False
buttonvar = Button.left
keygrab = False

frame = Tk.Frame(window, width=800, height=400)
frame.pack()

category = Tk.Label(frame,text="Click Speed")
category.config(font=("Helvetica",15))
category.place(x=0,y=20,width=100,height=20)

S = Tk.Text(frame,height=1,width=4)
S.insert("1.0", "7")
S.place(x=30,y=50)

seconds = Tk.Label(frame,text="CPS")
seconds.config(font=("Helvetica",10))
seconds.place(x=60,y=50,width=50,height=20)

data = 1 / int(S.get("1.0",'end-1c'))

def Update():
    global data
    try:
        temp = int(S.get("1.0",'end-1c'))
    except:
        notice.config(text=f"Failed",font=("Helvetica",20))
        print("Please use integers only.")
        return
    if temp > 999:
        notice.config(text=f"Failed",font=("Helvetica",20))
        print("Please use only 3 digits.")
        return
    data = 1 / temp
    global buttonvar
    if buttontype.get() == "Left":
        buttonvar = Button.left
    elif buttontype.get() == "Right":
        buttonvar = Button.right
    notice.config(text=f"{buttontype.get()} click {temp} CPS",font=("Helvetica",20))
    print(f"Updated to {buttontype.get()} click {temp} CPS")

setbutton = Tk.Button(frame,text="Update",font=("Helvetica",12),command=Update)
setbutton.place(x=120,y=50,width=60,height=20)

buttontype = Tk.StringVar(frame)
buttontype.set("Left")

buttonmenu = Tk.OptionMenu(frame, buttontype, "Left", "Right")
buttonmenu.config(font=("Helvetica",12))
buttonmenu.place(x=180,y=50,width=55,height=20)

notice = Tk.Label(frame,text="Fluctuates to prevent ban")
notice.config(font=("Helvetica",20))
notice.place(x=225,y=350,width=350,height=30)

title = Tk.Label(frame,text=f"Hypixel Autoclicker v{version}")
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
        global active
        times = 0
        speed = data
        while True:
            if window_closed:
                break
            if active:
                speed = data + (random.uniform(data / -9533,data / 14300))
                if times == 0:
                    speed = data + (data / 8)
                elif times == 1:
                    speed = data + (data / 6)
                elif times == 2:
                    speed = data + (data / 4)
                elif times == 3:
                    speed = data + (data / 2)
                times += 1
                mouse.press(buttonvar)
                time.sleep(0.001)
                mouse.release(buttonvar)
                time.sleep(speed)
            else:
                times = 0

task = Background()
task.daemon = True
task.start()

def remap():
    global keygrab
    keygrab = True
    while True:
        if not keygrab or window_closed:
            break
    keyname = str(COMBINATIONS[0]).split(":")[0].replace("{<Key.","").capitalize()
    remapbutton.config(text=f"Activate Key: {keyname}")
    notice.config(text=f"Press {keyname} to start")

remapbutton = Tk.Button(frame,text="Activate Key: F6",font=("Helvetica",12),command=remap)
remapbutton.place(x=120,y=80,width=130,height=20)

def execute():
    global active
    active = not active

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    global keygrab
    global COMBINATIONS
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
    elif keygrab:
        COMBINATIONS = []
        COMBINATIONS.append({key})
        keygrab = False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)

listener.start()
window.mainloop()
active = False
window_closed = True
