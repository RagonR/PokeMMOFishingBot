import ctypes
import time
from threading import *
from tkinter import *
from tkinter import messagebox, font
import random

import PIL
import pyautogui
from PIL import ImageGrab, ImageOps, ImageTk, Image
from numpy import array, os
SendInput = ctypes.windll.user32.SendInput
random.seed(time.time())

class Cordinates():
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    # LoginToGame
    FullScreen = (1856, 41)
    LoginBtn = (1062, 584)
    LoginBtn1 = (1044, 479)
    # Setup
    SettingX = (1060)
    SettingY = (485)
    GameplX = (705)
    GameplY = (455)
    Other = (700, 590)


class Pokemones():
    catchHor = 0
    catchMag = 0
    catchKra = 0
    Horsea = 0
    Magikarp = 0
    Krabby = 0
    HealTime = 0
    Button = ''
    Pokeballs = 0
    TillHeal = 0
    Rod = ''
    Stop = 0
    timeclock = 0
    guiClosed = 0


class BotMain(Thread):
    def run(self):
        if Pokemones.Pokeballs > 0:
            while Pokemones.Pokeballs > 0:
                if Pokemones.Stop == 1:
                    break
                catching()
                Pokemones.HealTime += 1
                if Pokemones.HealTime >= Pokemones.TillHeal:
                    ToHeal()
                    Pokemones.HealTime = 0


class BotInfoBar(Thread):
    def run(self):
        #
        # def __init__(self):
        # Frame.__init__(self)
        frame = Tk()
        frame.title('Live info')
        frame.configure(bg="#87DEF2")
        frame.geometry("170x120")
        frame.wm_attributes("-topmost", 1)
        # frame = Frame()
        # frame.grid()
        frame.configure(bg="#87DEF2")
        font10 = font.Font(family="Yu Gothic", size=10, weight='bold')
        font9 = font.Font(family="Yu Gothic", size=9, weight='bold')
        # Simple status flag
        # Our time structure [min, sec, centsec]
        timer = [0, 0, 0]
        # The format is padding all the
        pattern = '{0:02d}:{1:02d}:{2:02d}'
        # Create a timeText Label (a text box)
        Info = Label(frame, text="Run time:", font=font10, bg="#87DEF2")
        Info.grid(row=0, column=0)
        timeText = Label(frame, text="00:00:00", font=font10, bg="#87DEF2")
        timeText.grid(row=0, column=1)
        cList = Label(frame, text="Caught list", font=font10, bg="#87DEF2")
        cList.grid(row=1, column=0)
        Horsea = Label(frame, text="Horsea:", font=font9, bg="#87DEF2")
        Horsea.grid(row=2, column=0, sticky=E + N)
        CaughtH = Label(frame, text="00:00:00", font=font9, bg="#87DEF2")
        CaughtH.grid(row=2, column=1, sticky=W)
        Magikarp = Label(frame, text="Magikarp:", font=font9, bg="#87DEF2")
        Magikarp.grid(row=3, column=0, sticky=E)
        CaughtM = Label(frame, text="00", font=font9, bg="#87DEF2")
        CaughtM.grid(row=3, column=1, sticky=W)
        Krabby = Label(frame, text="Krabby:", font=font9, bg="#87DEF2")
        Krabby.grid(row=4, column=0, sticky=E + N)
        CaughtK = Label(frame, text="00", font=font9, bg="#87DEF2")
        CaughtK.grid(row=4, column=1, sticky=W)

        def exist():
            Pokemones.Stop = 1
            saveHistory()
            frame.destroy()

        quitButton = Button(frame, text='Quit', command=exist, font=font10, bg="#87DEF2")
        quitButton.grid(row=3, column=3, sticky=W)

        def updade_CaughtList():
            CaughtH.configure(text=Pokemones.Horsea)
            CaughtM.configure(text=Pokemones.Magikarp)
            CaughtK.configure(text=Pokemones.Krabby)
            frame.after(100, updade_CaughtList)

        def update_timeText():
            # Bot run Timer
            # Every time this function is called,
            # Increment 1 centisecond (1/100 of a second)
            timer[2] += 1
            # Every 100 centisecond is equal to 1 second
            if timer[2] >= 100:
                timer[2] = 0
                timer[1] += 1
            # Every 60 seconds is equal to 1 min
            if timer[1] >= 60:
                timer[0] += 1
                timer[1] = 0
            # Timer string
            timeString = pattern.format(timer[0], timer[1], timer[2])
            # Update the timeText Label box with the current time
            timeText.configure(text=timeString)
            # Call the update_timeText() function after 1 centisecond
            frame.after(10, update_timeText)

        update_timeText()
        updade_CaughtList()
        frame.mainloop()


class botInterface(Frame):
    def __init__(self):
        Frame.__init__(self)
        frame = Frame()
        self.master.title('Fishing bot')
        self.master.geometry("500x440")
        self.master.configure(bg="#87DEF2")
        frame.grid()
        font11 = font.Font(family="Yu Gothic", size=11, weight='bold')
        frame.configure(bg="#87DEF2")
        # Logotipas
        self.img = ImageTk.PhotoImage(PIL.Image.open("Logo.bmp"))
        self.logo = Label(frame, image=self.img, bg="white")
        self.logo.grid(row=0, columnspan=4)
        # Pokebolai
        self.labBalls = Label(frame, text="Amount of pokebolls:", bg="#87DEF2", font=font11)
        self.labBalls.grid(row=1, columnspan=1, sticky=W)
        self.pokeb = Entry(frame, width=4, bg="white")
        self.pokeb.grid(row=1, columnspan=1, sticky=E)
        # Skaicius
        self.labHeal = Label(frame, text="Number of battles until healing:", bg="#87DEF2", font=font11)
        self.labHeal.grid(row=1, column=2, sticky=W)
        self.heal = Entry(frame, width=4, bg="white")
        self.heal.grid(row=1, column=2, sticky=E)
        # Migtukas meskeres
        self.labRod = Label(frame, text="Fishing rod button:", bg="#87DEF2", font=font11)
        self.labRod.grid(row=2, columnspan=1, sticky=W)
        self.rod = Entry(frame, width=4, bg="white")
        self.rod.grid(row=2, columnspan=1, sticky=E)
        # Info
        self.labKill = Label(frame, text="List of pokemons: Catch/Kill (BOT MADE FOR 'Good Rod')", bg="#87DEF2",
                             font=font11)
        self.labKill.grid(row=3, columnspan=3, sticky=W)

        self.labInfo = Label(frame, text="(Check the box to catch that pokemon)", bg="#87DEF2", font=font11)
        self.labInfo.grid(row=4, columnspan=3, sticky=W + N)
        # Checkbox
        self.Horsea = IntVar()
        self.Horbut = Checkbutton(frame, bg="#87DEF2", text="Horsea    ", variable=self.Horsea, font=font11, onvalue=1,
                                  offvalue=0)
        self.Horbut.grid(row=6, column=0, sticky=W + E)
        self.Magikarp = IntVar()
        self.MagBut = Checkbutton(frame, bg="#87DEF2", text="Magikarp", variable=self.Magikarp, font=font11, onvalue=1,
                                  offvalue=0)
        self.MagBut.grid(row=7, column=0, sticky=W + E)
        self.Krabby = IntVar()
        self.KarBut = Checkbutton(frame, bg="#87DEF2", text="Karbby    ", variable=self.Krabby, font=font11, onvalue=1,
                                  offvalue=0)
        self.KarBut.grid(row=8, column=0, sticky=W + E)
        # Settup
        self.labAtt = Label(frame, text="<ATTENTION>", bg="#87DEF2", font=font11)
        self.labAtt.grid(row=6, column=2, sticky=S)

        self.labFor = Label(frame, text="        For first time launch, press:", bg="#87DEF2", font=font11)
        self.labFor.grid(row=7, column=2, sticky=N + W)

        # Buttons
        def History(event):
            filepath = 'History.txt'
            os.startfile(filepath)

        self.Hist = Button(frame, text="History", font=font11)
        self.Hist.bind("<ButtonRelease-1>", History)
        self.Hist.grid(row=11, column=0, sticky=S)

        def clickSetup(event):
            openesc()
            setup()

        self.settupButton = Button(frame, text="SETUP", font=font11)
        self.settupButton.bind("<ButtonRelease-1>", clickSetup, )
        self.settupButton.grid(row=8, column=2)

        def clickStart(event):
            try:
                Pokemones.Pokeballs = int(self.pokeb.get())
                try:
                    Pokemones.TillHeal = int(self.heal.get())
                    Pokemones.Rod = self.rod.get()
                    Pokemones.catchHor = self.Horsea.get()
                    Pokemones.catchMag = self.Magikarp.get()
                    Pokemones.catchKra = self.Krabby.get()
                    Pokemones.guiClosed = 1
                    self.master.destroy()
                except ValueError:
                    messagebox.showerror("Error", "With 'Number of battles until healing' please write numbers only")
            except ValueError:
                messagebox.showerror("Error", "With 'Amount of pokebolls' please write numbers only")

        self.StartButton = Button(frame, text=" Start ", font=font11)
        self.StartButton.bind("<ButtonRelease-1>", clickStart)
        self.StartButton.grid(row=10, column=0, sticky=N)

        # Load
        def clickLoad(event):
            loadsetting()
            messagebox.showinfo("Load", "Loaded successfully")
            Pokemones.guiClosed = 1
            self.master.destroy()

        self.settupButton = Button(frame, text="Load last time used setting", font=font11)
        self.settupButton.bind("<ButtonRelease-1>", clickLoad)
        self.settupButton.grid(row=11, column=2, sticky=S)


def Botinfo():
    BotInfoBar().mainloop()


def Gui():
    botInterface().mainloop()


def keyboardCodes(button):
    button = button.upper()
    if button == 'ESC':
        return 0x01
    if button == 'W':
        return 0x11
    elif button == 'E':
        return 0x12
    elif button == 'R':
        return 0x13
    elif button == 'T':
        return 0x14
    elif button == 'Y':
        return 0x15
    elif button == 'U':
        return 0x16
    elif button == 'I':
        return 0x17
    elif button == 'O':
        return 0x18
    elif button == 'P':
        return 0x19
    elif button == 'ENTER':
        return 0x1C
    elif button == 'A':
        return 0x1E
    elif button == 'S':
        return 0x1F
    elif button == 'D':
        return 0x20
    elif button == 'F':
        return 0x21
    elif button == 'G':
        return 0x22
    elif button == 'H':
        return 0x23
    elif button == 'J':
        return 0x24
    elif button == 'K':
        return 0x25
    elif button == 'L':
        return 0x26
    elif button == 'Z':
        return 0x2C
    elif button == 'X':
        return 0x2D
    elif button == 'C':
        return 0x2E
    elif button == 'V':
        return 0x2F
    elif button == 'B':
        return 0x30
    elif button == 'N':
        return 0x31
    elif button == 'M':
        return 0x32
    elif button == 'F1':
        return 0x3B
    elif button == 'F2':
        return 0x3C
    elif button == 'F3':
        return 0x3D
    elif button == 'F4':
        return 0x3E
    elif button == 'F5':
        return 0x3F
    elif button == 'F6':
        return 0x40
    elif button == 'F7':
        return 0x41
    elif button == 'F8':
        return 0x42
    elif button == 'F9':
        return 0x43
    elif button == 'F10':
        return 0x44
    elif button == 'F11':
        return 0x57
    elif button == 'F12':
        return 0x58
    else:
        messagebox.showerror("Error", "One of selected buttons is invalid")
        return False


# SendButton
def Send(button):
    button_code = keyboardCodes(button)
    if button_code is not False:
        button_hold_time = random.randint(598, 1535) / 1000
        PressKey(button_code)
        time.sleep(button_hold_time)
        ReleaseKey(button_code)
    else:
        Pokemones.Stop = 1



# Login to game
def logintogame():
    pyautogui.click(Cordinates.FullScreen)
    Send('Enter')
    time.sleep(1.5)
    Send('Enter')
    time.sleep(1.5)
    Send('Enter')
    time.sleep(1)
    Send('Enter')
    time.sleep(3)


# Open Setting
def openesc():
    pyautogui.click(Cordinates.FullScreen)
    pyautogui.click(Cordinates.FullScreen)
    Send('esc')
    Send('s')
    Send('enter')


# Setup functions
def searchcor(p1):
    box = (p1.X, p1.Y, p1.X + 40, p1.Y + 25)
    image = ImageGrab.grab(box)
    grayImage = ImageOps.grayscale(image)
    a = array(grayImage.getcolors())
    return a.sum()


def gamep():
    pyautogui.click(Cordinates.GameplX, Cordinates.GameplY)
    time.sleep(0.1)
    pyautogui.click(Cordinates.GameplX + 490, Cordinates.GameplY - 95)
    pyautogui.click(Cordinates.GameplX + 490, Cordinates.GameplY - 95)
    pyautogui.click(Cordinates.GameplX + 490, Cordinates.GameplY - 95)


def oth():
    pyautogui.click(Cordinates.Other)
    time.sleep(0.1)


# Setup check
def setup():
    # Pakeicia anti aliesing i 0
    p1 = Cordinates(1060, 485)
    while True:
        time.sleep(0.01)
        if searchcor(p1) < 13000:
            pyautogui.click(Cordinates.SettingX - 85, Cordinates.SettingY + 10)
        else:
            break
    # Isjungia overworld in battle
    p1 = Cordinates(1060, 555)
    if searchcor(p1) > 2700:
        pyautogui.click(Cordinates.SettingX, Cordinates.SettingY + 70)
    # Isjungia Battle Background
    p1 = Cordinates(1060, 590)
    p1 = Cordinates(1060, 590)
    if searchcor(p1) > 2600:
        pyautogui.click(Cordinates.SettingX, Cordinates.SettingY + 105)
    # Padaro battle window size: 100
    pyautogui.click(Cordinates.SettingX, Cordinates.SettingY + 181)
    time.sleep(1)
    pyautogui.typewrite('900')
    # Isjungia UI Effects
    p1 = Cordinates(1060, 690)
    if searchcor(p1) > 2800:
        pyautogui.click(Cordinates.SettingX, Cordinates.SettingY + 205)
    # Atidaro per Settings Gameplay ir padaro text speed i 4
    gamep()
    # Isjungia Chat bubbles
    p1 = Cordinates(1065, 380)
    print(searchcor(p1))
    if searchcor(p1) > 2850:
        pyautogui.click(Cordinates.SettingX, Cordinates.SettingY - 95)
    # Ijungia Toggle running
    p1 = Cordinates(1065, 425)
    if searchcor(p1) < 2300:
        pyautogui.click(Cordinates.SettingX, Cordinates.SettingY - 55)
    # Isjungia Own overworld name
    p1 = Cordinates(1065, 465)
    if searchcor(p1) > 2550:
        pyautogui.click(Cordinates.SettingX, Cordinates.SettingY - 15)
    # Atidaro per setting Other
    oth()
    # Pirma eile
    p1 = Cordinates(990, 385)
    if searchcor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(990, 420)
    if searchcor(p1) < 2800:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(990, 460)
    if searchcor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(990, 495)
    if searchcor(p1) < 2700:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(990, 535)
    if searchcor(p1) < 2500:
        pyautogui.click(p1.X, p1.Y)
    # Antra eile
    p1 = Cordinates(1075, 385)
    if searchcor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(1075, 460)
    if searchcor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(1075, 495)
    if searchcor(p1) < 2700:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(1075, 535)
    if searchcor(p1) < 2500:
        pyautogui.click(p1.X, p1.Y)
    # Trecia eile
    p1 = Cordinates(1160, 385)
    if searchcor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(1160, 420)
    if searchcor(p1) < 2800:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(1160, 460)
    if searchcor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(1160, 535)
    if searchcor(p1) < 2500:
        pyautogui.click(p1.X, p1.Y)
    p1 = Cordinates(1233, 750)
    pyautogui.click(p1.X, p1.Y)
    messagebox.showwarning("Worning", "If any setting were change please restart the game")
    messagebox.showwarning("Worning",
                           "Make sure that 'False Swipe' is first attack and to kill one second (best to use 20PP+)")


# Fishing
def checking(p1):
    box = (p1.X, p1.Y, p1.X + 30, p1.Y + 20)
    image = ImageGrab.grab(box)
    grayImage = ImageOps.grayscale(image)
    a = array(grayImage.getcolors())
    return a.sum()


def catching():
    err = 0
    pyautogui.click(Cordinates.FullScreen)
    pyautogui.click(Cordinates.FullScreen)
    Send(Pokemones.Rod)
    p1 = Cordinates(815, 395)
    print('Fishing')
    while True:
        if Pokemones.Stop == 1:
            break
        if searchcor(p1) < 1010:
            time.sleep(1)
            pokecheck()
            break
        time.sleep(0.05)
        if searchcor(p1) > 10000:
            Send('z')
            Send('z')
            err = 0
            time.sleep(0.1)
            Send(Pokemones.Rod)
        else:
            err += 1
            if err == 30:
                logintogame()
                catching()
                break
            Send('z')
            Send(Pokemones.Rod)


# Fighting
def catch():
    err = 0
    p1 = Cordinates(370, 685)
    print('Waiting to catch')
    while True:
        err += 1
        time.sleep(0.1)
        if err == 100:
            logintogame()
            catching()
            break
        if checking(p1) > 8000:
            print('Catching')
            Send('d')
            Send('z')
            Send('d')
            Send('d')
            Send('z')
            Pokemones.Pokeballs -= 1
            p1 = Cordinates(100, 280)
            print('Waiting For Battle To End')
            err = 0
            while True:
                err += 1
                if err >= 200:
                    logintogame()
                    catching()
                    break
                time.sleep(0.1)
                if checking(p1) > 1010:
                    closepop()
                    closepop()
                    break
            break


def attack():
    print('Attacking')
    Send('a')
    Send('z')
    Send('z')
    catch()


def kill():
    err = 0
    Send('a')
    Send('z')
    Send('d')
    Send('z')
    p1 = Cordinates(100, 280)
    while True:
        time.sleep(0.1)
        err += 1
        if err >= 200:
            logintogame()
            catching()
            break
        if searchcor(p1) > 1010:
            break


def pokecheck():
    p1 = Cordinates(335, 150)
    err = 0
    print('Looking For Pokemon')
    Send('z')
    while True:
        time.sleep(0.1)
        if checking(p1) < 10000 and checking(p1) > 5000:
            time.sleep(0.1)
            if checking(p1) < 10000 and checking(p1) > 5000:
                err = 0
                p1 = Cordinates(370, 685)
                print('Waiting to attack Horsea')
                while True:
                    err += 1
                    time.sleep(0.1)
                    if checking(p1) > 8000:
                        if Pokemones.catchHor == 0:
                            Pokemones.Horsea -= 1
                            kill()
                            break
                        else:
                            Pokemones.Horsea += 1
                            attack()
                            break
                    if err == 60:
                        logintogame()
                        catching()
                        break
                break
        elif checking(p1) > 12000:
            err = 0
            p1 = Cordinates(370, 685)
            print('Waiting to attack Magikarp')
            while True:
                time.sleep(0.1)
                if checking(p1) > 8000:
                    if Pokemones.catchMag == 0:
                        Pokemones.Magikarp -= 1
                        kill()
                        break
                    else:
                        Pokemones.Magikarp += 1
                        attack()
                        break
                if err == 60:
                    logintogame()
                    catching()
                    break
            break
        elif checking(p1) > 10000 and checking(p1) < 12000:
            err = 0
            p1 = Cordinates(370, 685)
            print('Waiting to attack Krabby')
            while True:
                time.sleep(0.1)
                if checking(p1) > 8000:
                    if Pokemones.catchKra == 0:
                        Pokemones.Krabby -= 1
                        kill()
                        break
                    else:
                        Pokemones.Krabby += 1
                        attack()
                        break
                if err == 60:
                    logintogame()
                    catching()
                    break
            break
        else:
            err += 1
            if err == 40:
                logintogame()
                catching()
                break


# Close popups
def closepop():
    p1 = Cordinates(965, 470)
    pyautogui.click(p1.X, p1.Y)
    time.sleep(0.01)
    Send('esc')
    p1 = Cordinates(935, 610)
    if checking(p1) > 8000:
        Send('enter')


# GoHealing; 0x11 = w button
def ToHeal():
    p1 = Cordinates(945, 340)
    while searchcor(p1) < 2700:
        PressKey('0x11')
    ReleaseKey(('0x11'))
    Heal()


# Healing
def Heal():
    ErrCheck = 0
    p1 = Cordinates(820, 270)
    Send('z')
    while True:
        time.sleep(0.15)
        if searchcor(p1) > 12000:
            Send('z')
            ErrCheck = 0
        else:
            ErrCheck += 1
            if ErrCheck >= 2:
                break
    time.sleep(1)
    FromHeal()


# BackHealing 0x1F = s button
def FromHeal():
    p1 = Cordinates(945, 550)
    while True:
        PressKey('0x1F')
        if searchcor(p1) < 1020:
            ReleaseKey('0x1F')
            time.sleep(1)
            break
    PressKey('0x1F')
    time.sleep(1)
    ReleaseKey('0x1F')


# Preset
def saveHistory():
    save_file = open("History.txt", "a+")
    save_file.write("\n\n")
    save_file.write("Horsea: ")
    save_file.write(str(Pokemones.Horsea))
    save_file.write(" Magikarp: ")
    save_file.write(str(Pokemones.Magikarp))
    save_file.write(" Krabby: ")
    save_file.write(str(Pokemones.Krabby))


def savesetting():
    save_file = open("save.txt", "w")
    save_file.write(str(Pokemones.Pokeballs))
    save_file.write(" ")
    save_file.write(str(Pokemones.TillHeal))
    save_file.write(" ")
    save_file.write(str(Pokemones.Rod))
    save_file.write(" ")
    save_file.write(str(Pokemones.catchHor))
    save_file.write(" ")
    save_file.write(str(Pokemones.catchMag))
    save_file.write(" ")
    save_file.write(str(Pokemones.catchKra))
    save_file.close()


def loadsetting():
    with open("save.txt", "r") as load:
        Pokemones.Pokeballs, Pokemones.TillHeal, Pokemones.Rod, Pokemones.catchHor, Pokemones.catchMag, Pokemones.catchKra = [
            str(x) for x in next(load).split()]
    load.close()
    Pokemones.Pokeballs = int(Pokemones.Pokeballs)
    Pokemones.TillHeal = int(Pokemones.TillHeal)
    Pokemones.catchHor = int(Pokemones.catchHor)
    Pokemones.catchMag = int(Pokemones.catchMag)
    Pokemones.catchKra = int(Pokemones.catchKra)


# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def main():
    Gui()
    Pokemones.timeclock = time.process_time()
    savesetting()
    Main = BotMain()
    Info = BotInfoBar()
    Main.start()
    if (Pokemones.guiClosed == 1):
        Info.start()

main()
