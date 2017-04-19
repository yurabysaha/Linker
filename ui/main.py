import Tkinter as tk

from ui.accept_view import Accept
from ui.connect_view import ConnectView
from ui.results import Results
from ui.settings import Settings

MAIN_BG = '#242424'

root = tk.Tk()
root.title('Yonchi')
root.configure(background=MAIN_BG)
root.resizable(width=False, height=False)
root.minsize(width=500, height=500)


menu = tk.Frame(root, bg=MAIN_BG)
body = tk.Frame(root, bg=MAIN_BG)
frames = {'body': body}
textfield = tk.Text(body, width=47, height=27, bg='#e6e6e6')
textfield.place(x=0, y=0)


def open_connect(event):
    for i in frames:
        frames[i].place_forget()
    ConnectView(frames, textfield, body)


def open_accept(event):
    for i in frames:
            frames[i].place_forget()
    Accept(frames, textfield, body)


def open_results(event):
    for i in frames:
            frames[i].place_forget()
    Results(root, frames)


def open_settings(event):
    for i in frames:
            frames[i].place_forget()
    Settings(root, frames)


class Menu:
    def __init__(self):
        self.process_btn = tk.Button(menu,
                                     text='Connect',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#e6e6e6', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.process_btn.bind("<Button-1>", open_connect)
        self.process_btn.place(x=0, y=2)

        self.accept_btn = tk.Button(menu,
                                     text='Accept',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#e6e6e6', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.accept_btn.bind("<Button-1>", open_accept)
        self.accept_btn.place(x=0, y=40)

        self.results_btn = tk.Button(menu,
                                    text='Results',
                                    highlightbackground=MAIN_BG,
                                    highlightcolor=MAIN_BG,
                                    bg='#e6e6e6', activebackground='#e6e6e6',
                                    borderwidth=0,
                                    highlightthickness=0,
                                    width=18, height=2)

        self.results_btn.bind("<Button-1>", open_results)
        self.results_btn.place(x=0, y=78)

        self.settings_btn = tk.Button(menu,
                                     text='Settings',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#e6e6e6', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.settings_btn.bind("<Button-1>", open_settings)
        self.settings_btn.place(x=0, y=116)


if __name__ == "__main__":
    menu.place(x=0, y=0, width=120, height=500)
    body.place(x=120, y=0, width=380, height=500)
    Menu()
    ConnectView(frames, textfield, body)
    root.mainloop()
