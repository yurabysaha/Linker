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
        self.count_today = data[0][0]
        self.count_all = data[1][0]
        tk.Label(self.body, text='Today     |     All ', bg='#e6e6e6').place(x=250, y=40)
        tk.Label(self.body, text='Accept connect', bg='#e6e6e6').place(x=250, y=10)
        self.counts = tk.Label(self.body, bg='#e6e6e6', text='%s     |     %s' % (self.count_today, self.count_all))
        self.counts.place(x=265, y=70)

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
        t = threading.Thread(target=Accept, args=(self.text, self))
        t.start()
        self.text.insert('end', "Start review connection people\n")

    def counts_update(self):
        self.count_today += 1
        self.count_all += 1
        self.counts.config(text='%s     |     %s' % (self.count_today, self.count_all))

    def counts_update_from_db(self):
        data = User().count_accepted()
        self.count_today = data[0][0]
        self.count_all = data[1][0]
        self.counts.config(text='%s     |     %s' % (self.count_today, self.count_all))
