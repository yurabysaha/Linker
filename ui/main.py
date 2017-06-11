#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import sys
import threading

import PIL

# from backup import Backup
from feed import Feed
from ui.accept_view import AcceptView
from ui.connect_view import ConnectView
from ui.forward_view import ForwardView
from ui.message_view import MessageView
from ui.results_view import ResultsView
from ui.settings_view import SettingsView

MAIN_BG = '#303030'

# Потрібно щоб не вискакувало вікно на віндовсі при закритті програми
# sys.stderr = open('error.log', 'w')
# sys.stdout = open('output.log', 'w')

root = tk.Tk()
root.title('Yonchi v 2.0')
root.iconbitmap(default='logo.ico')
root.configure(background=MAIN_BG)
root.resizable(width=False, height=False)
root.minsize(width=600, height=600)


menu = tk.Frame(root, bg=MAIN_BG)
body = tk.Frame(root, bg=MAIN_BG)
frames = {}
textfield = tk.Text(body, width=74, height=18, bg='#e6e6e6')
textfield.place(x=0, y=4)
menu_btns = []

view_obj = {}


def start_feed(event):
    t = threading.Thread(target=Feed)
    t.start()
root.bind("<Control-f>", start_feed)


def open_connect(event):
    active_menu_btn(event)
    for i in frames:
        frames[i].place_forget()
    frames['connect'].place(x=0, y=340, width=700, height=260)


def open_accept(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    if 'accept' not in frames:
        AcceptView(root, frames, textfield)
    else:
        frames['accept'].place(x=0, y=340, width=700, height=260)


def open_results(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    if 'results' not in frames:
        ResultsView(root, frames)
    else:
        frames['results'].place(x=0, y=340, width=700, height=260)


def open_message(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    if 'message' not in frames:
        message_view = MessageView(root, frames, textfield)
        view_obj['message_view'] = message_view
    else:
        frames['message'].place(x=0, y=340, width=700, height=260)
        t = threading.Thread(target=view_obj['message_view'].update_count_from_db)
        t.start()


def open_forward_message(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    if 'forward' not in frames:
        ForwardView(root, frames, textfield)
    else:
        frames['forward'].place(x=0, y=340, width=700, height=260)


def open_settings(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    if 'settings' not in frames:
        SettingsView(root, frames)
    else:
        frames['settings'].place(x=0, y=340, width=700, height=260)


def active_menu_btn(event):
    for i in menu_btns:
        i.config(bg='#eeeeee', fg='#000000')
    event.widget.config(bg='#616161', fg='#ffffff')


class Menu:
    def __init__(self):
        self.process_btn = tk.Button(menu,
                                     text='Connect',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=13, height=2)

        self.process_btn.bind("<Button-1>", open_connect)
        self.process_btn.place(x=1, y=0)
        menu_btns.append(self.process_btn)

        self.accept_btn = tk.Button(menu,
                                     text='Accept',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=13, height=2)

        self.accept_btn.bind("<Button-1>", open_accept)
        self.accept_btn.place(x=101, y=0)
        menu_btns.append(self.accept_btn)

        self.results_btn = tk.Button(menu,
                                    text='Results',
                                    highlightbackground=MAIN_BG,
                                    highlightcolor=MAIN_BG,
                                    bg='#eeeeee', activebackground='#e6e6e6',
                                    borderwidth=0,
                                    highlightthickness=0,
                                    width=13, height=2)

        self.results_btn.bind("<Button-1>", open_results)
        self.results_btn.place(x=201, y=0)
        menu_btns.append(self.results_btn)

        self.message_btn = tk.Button(menu,
                                     text='Message',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=13, height=2)

        self.message_btn.bind("<Button-1>", open_message)
        self.message_btn.place(x=301, y=0)
        menu_btns.append(self.message_btn)

        self.forward_message_btn = tk.Button(menu,
                                     text='Forward Message',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=13, height=2)

        self.forward_message_btn.bind("<Button-1>", open_forward_message)
        self.forward_message_btn.place(x=401, y=0)
        menu_btns.append(self.forward_message_btn)

        self.settings_btn = tk.Button(menu,
                                     text='Settings',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=13, height=2)

        self.settings_btn.bind("<Button-1>", open_settings)
        self.settings_btn.place(x=501, y=0)
        menu_btns.append(self.settings_btn)

if __name__ == "__main__":
    body.place(x=0, y=0, width=700, height=300)
    menu.place(x=0, y=300, width=700, height=300)
    menu = Menu()
    menu.process_btn.config(bg='#616161', fg='#ffffff')
    ConnectView(root, frames, textfield)
    # Backup().send_backup_to_email()
    root.mainloop()
