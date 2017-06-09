import Tkinter as tk
import threading
from user import User
from accept import Accept


class AcceptView:
    def __init__(self, root, frames, textfield):
        self.text = textfield
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['accept'] = self.body
        self.body.place(x=0, y=340, width=700, height=260)
        data = User().count_accepted()
        tk.Label(self.body, text='Today     |     All ', bg='#e6e6e6').place(x=250, y=40)
        tk.Label(self.body, text='Accept connect', bg='#e6e6e6').place(x=250, y=10)
        tk.Label(self.body, bg='#e6e6e6', text='%s     |     %s' % (data[0][0], data[1][0])).place(x=270, y=70)
        self.accept_btn = tk.Button(self.body,
                                     text='Start review',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=14, height=2)

        self.accept_btn.bind("<Button-1>", self.start_review)
        self.accept_btn.place(x=250, y=200)

    def start_review(self, event):
        self.accept_btn.unbind("<Button 1>")
        self.accept_btn.config(state='disabled')
        t = threading.Thread(target=Accept, args=(self.text,))
        t.start()
        self.text.insert('end', "Start review connection people\n")
