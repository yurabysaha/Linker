import Tkinter as tk
import threading
from connect import Connect


class ConnectView:
    def __init__(self, frames, textfield, body):

        self.text = textfield
        self.body = body
        frames['body'] = self.body
        self.body.place(x=120, y=0, width=380, height=500)

        self.results_btn = tk.Button(self.body,
                                     text='Start connect',
                                     bg='#e6e6e6', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.results_btn.bind("<Button-1>", self.start_connect)
        self.results_btn.place(x=130, y=450)

    def start_connect(self, event):
            t = threading.Thread(target=Connect, args=(self.text,))
            t.start()
            self.text.insert('end', "Start connect people\n")
