#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import sys

import PIL
from PIL import Image, ImageTk

from backup import Backup
from ui.accept_view import AcceptView
from ui.connect_view import ConnectView
from ui.forward_view import ForwardView
from ui.message_view import MessageView
from ui.results_view import ResultsView
from ui.settings_view import SettingsView

MAIN_BG = '#303030'

# Потрібно щоб не вискакувало вікно на віндовсі при закритті програми
sys.stderr = open('error.log', 'w')
sys.stdout = open('output.log', 'w')

root = tk.Tk()
root.title('Yonchi v 1.1.2')
root.iconbitmap(default='logo.ico')
root.configure(background=MAIN_BG)
root.resizable(width=False, height=False)
root.minsize(width=500, height=500)


menu = tk.Frame(root, bg=MAIN_BG)
body = tk.Frame(root, bg=MAIN_BG)
frames = {'logging': body}
textfield = tk.Text(body, width=47, height=30, bg='#e6e6e6')
textfield.place(x=0, y=4)
menu_btns = []


def open_logging(event):
    active_menu_btn(event)
    for i in frames:
        frames[i].place_forget()
    body.place(x=120, y=0, width=380, height=500)


def open_connect(event):
    active_menu_btn(event)
    for i in frames:
        frames[i].place_forget()
    ConnectView(root, frames, textfield)


def open_accept(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    AcceptView(root, frames, textfield)


def open_results(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    ResultsView(root, frames)


def open_message(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    MessageView(root, frames, textfield)


def open_forward_message(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    ForwardView(root, frames, textfield)


def open_settings(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    SettingsView(root, frames)


def active_menu_btn(event):
    for i in menu_btns:
        i.config(bg='#eeeeee', fg='#000000')
    event.widget.config(bg='#616161', fg='#ffffff')

class Menu:
    def __init__(self):
        self.logging_btn = tk.Button(menu,
                                     text='Process log',
                                     highlightbackground=MAIN_BG,
                                     bg='#eeeeee', activebackground=MAIN_BG,
                                     highlightcolor='#ff5722',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.logging_btn.bind("<Button-1>", open_logging)
        self.logging_btn.place(x=0, y=2)
        menu_btns.append(self.logging_btn)

        self.process_btn = tk.Button(menu,
                                     text='Connect',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.process_btn.bind("<Button-1>", open_connect)
        self.process_btn.place(x=0, y=40)
        menu_btns.append(self.process_btn)

        self.accept_btn = tk.Button(menu,
                                     text='Accept',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.accept_btn.bind("<Button-1>", open_accept)
        self.accept_btn.place(x=0, y=78)
        menu_btns.append(self.accept_btn)

        self.results_btn = tk.Button(menu,
                                    text='Results',
                                    highlightbackground=MAIN_BG,
                                    highlightcolor=MAIN_BG,
                                    bg='#eeeeee', activebackground='#e6e6e6',
                                    borderwidth=0,
                                    highlightthickness=0,
                                    width=18, height=2)

        self.results_btn.bind("<Button-1>", open_results)
        self.results_btn.place(x=0, y=116)
        menu_btns.append(self.results_btn)

        self.message_btn = tk.Button(menu,
                                     text='Message',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.message_btn.bind("<Button-1>", open_message)
        self.message_btn.place(x=0, y=154)
        menu_btns.append(self.message_btn)

        self.forward_message_btn = tk.Button(menu,
                                     text='Forward Message',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.forward_message_btn.bind("<Button-1>", open_forward_message)
        self.forward_message_btn.place(x=0, y=192)
        menu_btns.append(self.forward_message_btn)

        self.settings_btn = tk.Button(menu,
                                     text='Settings',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.settings_btn.bind("<Button-1>", open_settings)
        self.settings_btn.place(x=0, y=230)
        menu_btns.append(self.settings_btn)

        # Logo
        im = PIL.Image.open("logo.png")
        photo = PIL.ImageTk.PhotoImage(im)
        b = tk.Label(menu, image=photo, bg=MAIN_BG)
        b.image = photo
        b.place(x=8, y=310)

if __name__ == "__main__":
    menu.place(x=0, y=0, width=120, height=500)
    body.place(x=120, y=0, width=380, height=500)
    Menu()
    Backup().send_backup_to_email()
    root.mainloop()
