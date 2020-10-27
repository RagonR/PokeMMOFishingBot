import ctypes
import time
from threading import *
from tkinter import *
from tkinter import messagebox, font, Label
import random

import PIL
import pyautogui
from PIL import ImageGrab, ImageOps, ImageTk, Image
from numpy import array, os

SendInput = ctypes.windll.user32.SendInput
random.seed(time.time())


class Coordinates():
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    # LoginToGame
    fullscreen = (1856, 41)
    login_btn = (1062, 584)
    login_btn1 = (1044, 479)
    # Setup
    setting_x = 1060
    setting_y = 485
    gamepl_x = 705
    gamepl_y = 455
    Other = (700, 590)


class Pokemones():
    catchHor = 0
    catchMag = 0
    catchKra = 0
    horsea = 0
    magikarp = 0
    krabby = 0
    HealTime = 0
    Button = ''
    pokeballs = 0
    till_heal = 0
    Rod = ''
    Stop = 0
    time_clock = 0
    gui_closed = 0


class Bot_Main(Thread):
    def run(self):
        if Pokemones.pokeballs > 0:
            while Pokemones.pokeballs > 0:
                if Pokemones.Stop == 1:
                    break
                catching()
                Pokemones.HealTime += 1
                if Pokemones.HealTime >= Pokemones.till_heal:
                    to_heal()
                    Pokemones.HealTime = 0


class Bot_Info_Bar(Thread):
    def run(self):
        frame = Tk()
        frame.title('Live info')
        frame.configure(bg="#87DEF2")
        frame.geometry("170x120")
        frame.wm_attributes("-topmost", 1)
        frame.configure(bg="#87DEF2")
        font10 = font.Font(family="Yu Gothic", size=10, weight='bold')
        font9 = font.Font(family="Yu Gothic", size=9, weight='bold')
        # Simple status flag
        # Our time structure [min, sec, centsec]
        timer = [0, 0, 0]
        # The format is padding all the
        pattern = '{0:02d}:{1:02d}:{2:02d}'
        # Create a timeText Label (a text box)
        info = Label(frame, text="Run time:", font=font10, bg="#87DEF2")
        info.grid(row=0, column=0)
        time_text = Label(frame, text="00:00:00", font=font10, bg="#87DEF2")
        time_text.grid(row=0, column=1)
        catch_list = Label(frame, text="Caught list", font=font10, bg="#87DEF2")
        catch_list.grid(row=1, column=0)
        horsea: Label = Label(frame, text="Horsea:", font=font9, bg="#87DEF2")
        horsea.grid(row=2, column=0, sticky=E + N)
        caughtH = Label(frame, text="00:00:00", font=font9, bg="#87DEF2")
        caughtH.grid(row=2, column=1, sticky=W)
        magikarp = Label(frame, text="Magikarp:", font=font9, bg="#87DEF2")
        magikarp.grid(row=3, column=0, sticky=E)
        caughtM = Label(frame, text="00", font=font9, bg="#87DEF2")
        caughtM.grid(row=3, column=1, sticky=W)
        krabby = Label(frame, text="Krabby:", font=font9, bg="#87DEF2")
        krabby.grid(row=4, column=0, sticky=E + N)
        caughtK = Label(frame, text="00", font=font9, bg="#87DEF2")
        caughtK.grid(row=4, column=1, sticky=W)

        def exist():
            Pokemones.Stop = 1
            save_history()
            frame.destroy()

        quit_button = Button(frame, text='Quit', command=exist, font=font10, bg="#87DEF2")
        quit_button.grid(row=3, column=3, sticky=W)

        def update_caught_list():
            caughtH.configure(text=Pokemones.horsea)
            caughtM.configure(text=Pokemones.magikarp)
            caughtK.configure(text=Pokemones.krabby)
            frame.after(100, update_caught_list)

        def update_time_text():
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
            time_string = pattern.format(timer[0], timer[1], timer[2])
            # Update the timeText Label box with the current time
            time_text.configure(text=time_string)
            # Call the update_time_text() function after 1 centisecond
            frame.after(10, update_time_text)

        update_time_text()
        update_caught_list()
        frame.mainloop()

    def mainloop(self):
        pass


class Bot_Interface(Frame):
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
        def history(event):
            filename = 'history.txt'
            os.startfile(filename)

        self.Hist = Button(frame, text="history", font=font11)
        self.Hist.bind("<ButtonRelease-1>", history)
        self.Hist.grid(row=11, column=0, sticky=S)

        def click_setup(event):
            open_esc()
            setup()

        self.settupButton = Button(frame, text="SETUP", font=font11)
        self.settupButton.bind("<ButtonRelease-1>", click_setup, )
        self.settupButton.grid(row=8, column=2)

        def click_start(event):
            try:
                Pokemones.pokeballs = int(self.pokeb.get())
                try:
                    Pokemones.till_heal = int(self.heal.get())
                    Pokemones.Rod = self.rod.get()
                    Pokemones.catchHor = self.Horsea.get()
                    Pokemones.catchMag = self.Magikarp.get()
                    Pokemones.catchKra = self.Krabby.get()
                    Pokemones.gui_closed = 1
                    self.master.destroy()
                except ValueError:
                    messagebox.showerror("Error", "With 'Number of battles until healing' please write numbers only")
            except ValueError:
                messagebox.showerror("Error", "With 'Amount of pokebolls' please write numbers only")

        self.StartButton = Button(frame, text=" Start ", font=font11)
        self.StartButton.bind("<ButtonRelease-1>", click_start)
        self.StartButton.grid(row=10, column=0, sticky=N)

        # Load
        def click_load(event):
            load_setting()
            messagebox.showinfo("Load", "Loaded successfully")
            Pokemones.gui_closed = 1
            self.master.destroy()

        self.settupButton = Button(frame, text="Load last time used setting", font=font11)
        self.settupButton.bind("<ButtonRelease-1>", click_load)
        self.settupButton.grid(row=11, column=2, sticky=S)


def run_bot_info():
    Bot_Info_Bar().mainloop()


def run_gui():
    Bot_Interface().mainloop()


def keyboard_codes(button):
    button = button.upper()
    if button == 'ESC':
        return 0x01
    elif button == 'W':
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
        messagebox.showerror("Error", "One of the selected buttons is invalid")
        return False


# SendButton
def send_keyboard_input(button):
    button_code = keyboard_codes(button)
    if button_code is not False:
        button_hold_time = random.randint(198, 235) / 1000
        press_key(button_code)
        time.sleep(button_hold_time)
        release_key(button_code)
    else:
        Pokemones.Stop = 1


# Login to game
def login_into_the_game():
    pyautogui.click(Coordinates.fullscreen)

    wait = random.randint(898, 1335) / 1000
    print(wait)
    time.sleep(wait)
    for x in range(4):
        time.sleep(wait)
        send_keyboard_input('Enter')
        wait = random.randint(898, 1335) / 1000
        print(wait)
        time.sleep(wait)


# Open Setting
def open_esc():
    pyautogui.click(Coordinates.fullscreen)
    pyautogui.click(Coordinates.fullscreen)
    send_keyboard_input('esc')
    send_keyboard_input('s')
    send_keyboard_input('enter')


# Setup functions
def search_coor(p1):
    box = (p1.X, p1.Y, p1.X + 40, p1.Y + 25)
    image = ImageGrab.grab(box)
    grayImage = ImageOps.grayscale(image)
    a = array(grayImage.getcolors())
    return a.sum()


def gamep():
    pyautogui.click(Coordinates.gamepl_x, Coordinates.gamepl_y)
    time.sleep(0.1)
    pyautogui.click(Coordinates.gamepl_x + 490, Coordinates.gamepl_y - 95)
    pyautogui.click(Coordinates.gamepl_x + 490, Coordinates.gamepl_y - 95)
    pyautogui.click(Coordinates.gamepl_x + 490, Coordinates.gamepl_y - 95)


def oth():
    pyautogui.click(Coordinates.Other)
    time.sleep(0.1)


# Setup check
def setup():
    # Pakeicia anti aliesing i 0
    p1 = Coordinates(1060, 485)
    while True:
        time.sleep(0.01)
        if search_coor(p1) < 13000:
            pyautogui.click(Coordinates.setting_x - 85, Coordinates.setting_y + 10)
        else:
            break
    # Isjungia overworld in battle
    p1 = Coordinates(1060, 555)
    if search_coor(p1) > 2700:
        pyautogui.click(Coordinates.setting_x, Coordinates.setting_y + 70)
    # Isjungia Battle Background
    p1 = Coordinates(1060, 590)
    p1 = Coordinates(1060, 590)
    if search_coor(p1) > 2600:
        pyautogui.click(Coordinates.setting_x, Coordinates.setting_y + 105)
    # Padaro battle window size: 100
    pyautogui.click(Coordinates.setting_x, Coordinates.setting_y + 181)
    time.sleep(1)
    pyautogui.typewrite('900')
    # Isjungia UI Effects
    p1 = Coordinates(1060, 690)
    if search_coor(p1) > 2800:
        pyautogui.click(Coordinates.setting_x, Coordinates.setting_y + 205)
    # Atidaro per Settings Gameplay ir padaro text speed i 4
    gamep()
    # Isjungia Chat bubbles
    p1 = Coordinates(1065, 380)
    print(search_coor(p1))
    if search_coor(p1) > 2850:
        pyautogui.click(Coordinates.setting_x, Coordinates.setting_y - 95)
    # Ijungia Toggle running
    p1 = Coordinates(1065, 425)
    if search_coor(p1) < 2300:
        pyautogui.click(Coordinates.setting_x, Coordinates.setting_y - 55)
    # Isjungia Own overworld name
    p1 = Coordinates(1065, 465)
    if search_coor(p1) > 2550:
        pyautogui.click(Coordinates.setting_x, Coordinates.setting_y - 15)
    # Atidaro per setting Other
    oth()
    # Pirma eile
    p1 = Coordinates(990, 385)
    if search_coor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(990, 420)
    if search_coor(p1) < 2800:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(990, 460)
    if search_coor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(990, 495)
    if search_coor(p1) < 2700:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(990, 535)
    if search_coor(p1) < 2500:
        pyautogui.click(p1.X, p1.Y)
    # Antra eile
    p1 = Coordinates(1075, 385)
    if search_coor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(1075, 460)
    if search_coor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(1075, 495)
    if search_coor(p1) < 2700:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(1075, 535)
    if search_coor(p1) < 2500:
        pyautogui.click(p1.X, p1.Y)
    # Trecia eile
    p1 = Coordinates(1160, 385)
    if search_coor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(1160, 420)
    if search_coor(p1) < 2800:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(1160, 460)
    if search_coor(p1) < 2600:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(1160, 535)
    if search_coor(p1) < 2500:
        pyautogui.click(p1.X, p1.Y)
    p1 = Coordinates(1233, 750)
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
    pyautogui.moveTo(Coordinates.fullscreen)
    send_keyboard_input(Pokemones.Rod)
    p1 = Coordinates(815, 395)
    print('Fishing')
    while True:
        if Pokemones.Stop == 1:
            break
        if search_coor(p1) < 1010:
            time.sleep(1)
            poke_check()
            break
        time.sleep(0.05)
        if search_coor(p1) > 10000:
            send_keyboard_input('z')
            send_keyboard_input('z')
            err = 0
            time.sleep(0.1)
            send_keyboard_input(Pokemones.Rod)
        else:
            err += 1
            if err == 30:
                login_into_the_game()
                catching()
                break
            send_keyboard_input('z')
            send_keyboard_input(Pokemones.Rod)


# Fighting
def catch():
    err = 0
    p1 = Coordinates(370, 685)
    print('Waiting to catch')
    while True:
        err += 1
        time.sleep(0.1)
        if err == 100:
            login_into_the_game()
            catching()
            break
        if checking(p1) > 8000:
            throwing_pokeball()
            Pokemones.pokeballs -= 1
            p1 = Coordinates(100, 280)
            print('Waiting For Battle To End')
            err = 0
            while True:
                err += 1
                if err >= 200:
                    login_into_the_game()
                    catching()
                    break
                time.sleep(0.2)
                if checking(p1) > 1010:
                    close_popups()
                    print('Close popup')
                    break
            break


def throwing_pokeball():
    print('Throwing pokeball')
    send_keyboard_input('d')
    send_keyboard_input('z')
    send_keyboard_input('d')
    send_keyboard_input('d')
    send_keyboard_input('z')


def attack():
    print('Attacking')
    send_keyboard_input('a')
    send_keyboard_input('z')
    send_keyboard_input('z')
    catch()


def kill():
    err = 0
    send_keyboard_input('a')
    send_keyboard_input('z')
    send_keyboard_input('d')
    send_keyboard_input('z')
    p1 = Coordinates(100, 280)
    while True:
        time.sleep(0.1)
        err += 1
        if err >= 200:
            login_into_the_game()
            catching()
            break
        if search_coor(p1) > 1010:
            break


def poke_check():
    p1 = Coordinates(335, 150)
    err = 0
    print('Looking For Pokemon')
    send_keyboard_input('z')
    while True:
        time.sleep(0.1)
        if 10000 > checking(p1) > 5000:
            time.sleep(0.1)
            if 10000 > checking(p1) > 5000:
                err = 0
                p1 = Coordinates(370, 685)
                print('Waiting to attack Horsea')
                while True:
                    err += 1
                    time.sleep(0.1)
                    if checking(p1) > 8000:
                        if Pokemones.catchHor == 0:
                            Pokemones.horsea -= 1
                            kill()
                            break
                        else:
                            Pokemones.horsea += 1
                            attack()
                            break
                    if err == 60:
                        login_into_the_game()
                        catching()
                        break
                break
        elif checking(p1) > 12000:
            err = 0
            p1 = Coordinates(370, 685)
            print('Waiting to attack Magikarp')
            while True:
                time.sleep(0.1)
                if checking(p1) > 8000:
                    if Pokemones.catchMag == 0:
                        Pokemones.magikarp -= 1
                        kill()
                        break
                    else:
                        Pokemones.magikarp += 1
                        attack()
                        break
                if err == 60:
                    login_into_the_game()
                    catching()
                    break
            break
        elif 10000 < checking(p1) < 12000:
            err = 0
            p1 = Coordinates(370, 685)
            print('Waiting to attack Krabby')
            while True:
                time.sleep(0.1)
                if checking(p1) > 8000:
                    if Pokemones.catchKra == 0:
                        Pokemones.krabby -= 1
                        kill()
                        break
                    else:
                        Pokemones.krabby += 1
                        attack()
                        break
                if err == 60:
                    login_into_the_game()
                    catching()
                    break
            break
        else:
            err += 1
            if err == 40:
                login_into_the_game()
                catching()
                break


# Close popups
def close_popups():
    p1 = Coordinates(965, 470)
    pyautogui.click(p1.X, p1.Y)
    time.sleep(0.01)
    send_keyboard_input('esc')
    p1 = Coordinates(935, 610)
    if checking(p1) > 8000:
        send_keyboard_input('enter')


# GoHealing; 0x11 = w button
def to_heal():
    print("Going to pokecenter")
    p1 = Coordinates(945, 340)
    print(search_coor(p1))
    button = keyboard_codes("w")
    while search_coor(p1) < 2650:
        press_key(button)
    release_key(button)
    heal()


# Healing
def heal():
    print("Going to nurse")
    err_check = 0
    p1 = Coordinates(558, 140)
    send_keyboard_input('z')
    time.sleep(0.2)
    send_keyboard_input('z')
    print(search_coor(p1))
    while True:
        time.sleep(0.15)
        if search_coor(p1) > 12000:
            send_keyboard_input('z')
            err_check = 0
        else:
            err_check += 1
            if err_check >= 2:
                break
    time.sleep(1)
    from_heal()


# BackHealing 0x1F = s button
def from_heal():
    print("Going back to fishing")
    p1 = Coordinates(945, 550)
    while True:
        press_key(0x1F)
        if search_coor(p1) < 1020:
            release_key(0x1F)
            time.sleep(1)
            break
    button_hold_time = random.randint(698, 835) / 1000
    press_key(0x1F)
    time.sleep(button_hold_time)
    release_key(0x1F)


# Preset
def save_history():
    save_file = open("History.txt", "a+")
    save_file.write("\n\n")
    save_file.write("Horsea: ")
    save_file.write(str(Pokemones.horsea))
    save_file.write(" Magikarp: ")
    save_file.write(str(Pokemones.magikarp))
    save_file.write(" Krabby: ")
    save_file.write(str(Pokemones.krabby))


def save_setting():
    save_file = open("save.txt", "w")
    save_file.write(str(Pokemones.pokeballs))
    save_file.write(" ")
    save_file.write(str(Pokemones.till_heal))
    save_file.write(" ")
    save_file.write(str(Pokemones.Rod))
    save_file.write(" ")
    save_file.write(str(Pokemones.catchHor))
    save_file.write(" ")
    save_file.write(str(Pokemones.catchMag))
    save_file.write(" ")
    save_file.write(str(Pokemones.catchKra))
    save_file.close()


def load_setting():
    with open("save.txt", "r") as load:
        Pokemones.pokeballs, Pokemones.till_heal, Pokemones.Rod, Pokemones.catchHor, Pokemones.catchMag, Pokemones.catchKra = [
            str(x) for x in next(load).split()]
    load.close()
    Pokemones.pokeballs = int(Pokemones.pokeballs)
    Pokemones.till_heal = int(Pokemones.till_heal)
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


# Actual Functions
def press_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def main():
    run_gui()
    Pokemones.time_clock = time.process_time()
    save_setting()
    setup_gui = Bot_Main()
    bot_progress_gui = Bot_Info_Bar()
    setup_gui.start()
    if Pokemones.gui_closed == 1:
        bot_progress_gui.start()


main()