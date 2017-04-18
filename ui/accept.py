import Tkinter as tk


class Accept:
    def __init__(self, frames, textfield, body):
        self.text = textfield
        self.text.place(x=0, y=0)
        self.body = body
        frames['accept'] = self.body

        self.body.place(x=120, y=0, width=380, height=500)

        self.results_btn = tk.Button(self.body,
                                     text='Start review',
                                     bg='#e6e6e6', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.results_btn.bind("<Button-1>", self.start_review)
        self.results_btn.place(x=130, y=450)

    def start_review(self, event):
        self.text.insert('end', "Start review connection people\n")
