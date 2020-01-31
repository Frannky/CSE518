"""
file：magic.py
create time:2019/11/27 14:54
author:Hang Zhao
desc: project
"""

import tkinter as tk
from tkinter import filedialog, dialog
import os
import speech_recognition as sr
import pyautogui
from pynput.keyboard import Key, Controller
import pyperclip
import subprocess
import time
from docx import Document
from tkinter import *


window = tk.Tk()
window.title('HCI Project 1.0')
window.geometry('680x650')

file_path = ''

file_text = ''
label = tk.Label(window, width = 40, height = 3, text = 'Word Document Interactor',fg= "Brown")
label.pack()
text1 = tk.Text(window, width=45, height=5, bg='orange', font=('Calibri', 20))
text1.pack()

UserName = ""
working_path = ""

def create_file():

    document = Document()

    file_path = filedialog.asksaveasfilename(title=u'saving file')
    print(file_path)

    document.save(file_path + ".docx")

def select_file():
    global working_path
    working_path = filedialog.askopenfilename(title=u'working path')
    print(working_path)


def open_file():
    global file_path
    global file_text
    file_path = filedialog.askopenfilename(title=u'choose file',
                                           initialdir=(os.path.expanduser('/User')))
    print('open file：', file_path)
    if file_path is not None:
        subprocess.run(['open', file_path], check=True)


def save_file():
    global file_path
    global file_text
    file_path = filedialog.asksaveasfilename(title=u'save file')
    print('saving file：', file_path)
    file_text = text1.get('1.0', tk.END)
    if file_path is not None:
        with open(file=file_path, mode='a+', encoding='utf-8') as file:
            file.write(file_text)
        text1.delete('1.0', tk.END)
        dialog.Dialog(None, {'title': 'File Modified',
                             'text': 'finish saving',
                             'bitmap': 'warning', 'default': 0,
                             'strings': ('OK', 'Cancle')})
        print('finish saving file')

def modify_content():


    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Please say something....\n")
        text1.insert(INSERT, "Please say something....\n")
        audio = r.listen(source)
        ret = r.recognize_google(audio)
        print("The word you said is : ", ret)
        st = "The word you said is : " + ret + "\n"
        text1.insert(INSERT, st)

        pyperclip.copy(ret)
        time.sleep(2)

        pyautogui.doubleClick()

        keyboard = Controller()

        keyboard.press(Key.cmd.value)
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release(Key.cmd.value)
        pyautogui.typewrite(" ")

def modify_font():
    time.sleep(1)
    pyautogui.doubleClick()
    time.sleep(1)
    keyboard = Controller()
    with keyboard.pressed(Key.cmd.value):
        with keyboard.pressed(Key.shift):
            keyboard.press('.')
    keyboard.release('.')
    pyautogui.click()

    keyboard.release(Key.shift)
    keyboard.release(Key.cmd.value)


def modify_font1():
    time.sleep(1)
    pyautogui.doubleClick()
    time.sleep(1)
    keyboard = Controller()
    with keyboard.pressed(Key.cmd.value):
        with keyboard.pressed(Key.shift):
            keyboard.press(',')
    keyboard.release(',')
    pyautogui.click()

    keyboard.release(Key.shift)
    keyboard.release(Key.cmd.value)

def underline():
    time.sleep(1)
    pyautogui.doubleClick()
    time.sleep(1)
    keyboard = Controller()

    with keyboard.pressed(Key.cmd.value):
        keyboard.press('u')
    keyboard.release('u')
    pyautogui.click()

    keyboard.release(Key.cmd.value)

def bold():
    time.sleep(1)
    pyautogui.doubleClick()
    time.sleep(1)
    keyboard = Controller()

    with keyboard.pressed(Key.cmd.value):
        keyboard.press('b')
    keyboard.release('b')
    pyautogui.click()

    keyboard.release(Key.cmd.value)

def Italic():
    time.sleep(1)
    pyautogui.doubleClick()
    time.sleep(1)
    keyboard = Controller()

    with keyboard.pressed(Key.cmd.value):
        keyboard.press('i')
    keyboard.release('i')
    pyautogui.click()

    keyboard.release(Key.cmd.value)

def fun():


    while(1):
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:

            text1.insert(INSERT, "Please say something....\n")
            print("Please say something....")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            ret = r.recognize_google(audio)
            print("The word you said is : ", ret)
            if ret.lower() == "exit":
                text1.insert(INSERT, "Ending the program!\n")
                print("Ending the program!\n")
                break
            elif ret.lower() == "open file":
                text1.insert(INSERT, "Open a new file!\n")
                print("Open a new file!\n")
                open_file()
            elif ret.lower() == "save file":
                text1.insert(INSERT, "Save a file!\n")
                print("Save a file!\n")
                save_file()
            elif ret.lower() == "create file":
                text1.insert(INSERT, "Creating a new file!\n")
                print("Creating a new file!\n")
                create_file()
            elif ret.lower() == "make words bigger":
                text1.insert(INSERT, "Making font bigger!\n")
                print("Making font bigger!\n")
                modify_font()
            elif ret.lower() == "make words smaller":
                text1.insert(INSERT, "Making font smaller!\n")
                print("Making font smaller!\n")
                modify_font1()
            elif ret.lower() == "select working file":
                text1.insert(INSERT, "Selecting working file!\n")
                print("Selecting working file!\n")
                save_file()
            elif ret.lower() == "underline":
                text1.insert(INSERT, "Making underline!\n")
                print("Making underline!\n")
                underline()
            elif ret.lower() == "make words bold":
                text1.insert(INSERT, "Making words bold!\n")
                print("Making words bold!\n")
                bold()
            elif ret.lower() == "make words italic":
                text1.insert(INSERT, "Making words italic!\n")
                print("Making words italic!\n")
                Italic()
            elif ret.lower() == "magic":
                text1.insert(INSERT, "Making a magic!\n")
                print("Making a magic!\n")
                modify_content()
            else:
                continue

bt0 = tk.Button(window,text='voice control', width=15, height=2,command=fun,fg = "SaddleBrown")
bt0.place(x = 20, y = 190)
label0 = tk.Label(window, text = 'Using speech recognization to control each step!',fg= "Brown")
label0.place(x = 170, y = 197)

bt1 = tk.Button(window, text='open file', width=15, height=2, command=open_file,fg = "SaddleBrown")
bt1.place(x = 20, y = 230)
label1 = tk.Label(window, text = 'Speak : open file. Open word document from a directory!',fg="Brown")
label1.place(x = 170, y = 237)

bt2 = tk.Button(window, text='save file', width=15, height=2, command=save_file,fg = "SaddleBrown")
bt2.place(x = 20, y = 270)
label2 = tk.Label(window, text = 'Speak : save file. Save word document to a directory!',fg="Brown")
label2.place(x = 170, y = 277)

bt3 = tk.Button(window, text='create file', width=15, height=2, command=create_file,fg = "SaddleBrown")
bt3.place(x = 20, y = 310)
label3 = tk.Label(window, text = 'Speak : create file. Create word document in any directory!',fg="Brown")
label3.place(x = 170, y = 317)

bt4 = tk.Button(window, text='make font bigger', width=15, height=2, command=modify_font,fg = "SaddleBrown")
bt4.place(x = 20, y = 350)
label4 = tk.Label(window, text = 'Speak : make words bigger. Making selected words in document bigger!',fg="Brown")
label4.place(x = 170, y = 357)

bt5 = tk.Button(window, text='make font smaller', width=15, height=2, command=modify_font1,fg = "SaddleBrown")
bt5.place(x = 20, y = 390)
label5 = tk.Label(window, text = 'Speak : make words smaller. Making selected words in document smaller!',fg="Brown")
label5.place(x = 170, y = 397)

bt7 = tk.Button(window, text='underline', width=15, height=2, command=underline,fg = "SaddleBrown")
bt7.place(x = 20, y = 430)
label7 = tk.Label(window, text = 'Speak : underline. Making selected words underline!',fg="Brown")
label7.place(x = 170, y = 437)

bt8 = tk.Button(window, text='bold', width=15, height=2, command=bold,fg = "SaddleBrown")
bt8.place(x = 20, y = 470)
label8 = tk.Label(window, text = 'Speak : make words bold. Making selected words bold!',fg="Brown")
label8.place(x = 170, y = 477)

bt9 = tk.Button(window, text='italic', width=15, height=2, command=Italic,fg = "SaddleBrown")
bt9.place(x = 20, y = 510)
label9 = tk.Label(window, text = 'Speak : make words italic. Making selected words italic!',fg="Brown")
label9.place(x = 170, y = 517)

button = tk.Button(window, text = "magic", width=15,height=2, command = modify_content,fg = "SaddleBrown")
button.place(x = 20, y = 550)
label10 = tk.Label(window, text = 'Speak : magic. Changing the content to be the word recognized by speech!',fg="Brown")
label10.place(x = 170, y = 557)

bt6 = tk.Button(window, text='exit', width=15, height=2, command= exit,fg = "SaddleBrown")
bt6.place(x = 20, y = 590)
label6 = tk.Label(window, text = 'Speak : exit. Exit program!',fg="Brown")
label6.place(x = 170, y = 597)

window.mainloop()

