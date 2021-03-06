import Tkinter as tk
import tkMessageBox

import time

from results import Results


class ResultsView:
    def __init__(self, root, frames):

        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['results'] = self.body
        frames['results'].place(x=0, y=340, width=700, height=260)
        tk.Label(self.body, bg='#e6e6e6', text='Generate Report').place(x=240, y=3)
        self.results_btn = tk.Button(self.body,
                                     text='Today report',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#214312',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.results_btn.bind("<Button-1>", self.generate_report)
        self.results_btn.place(x=150, y=200)

        self.all_results_btn = tk.Button(self.body,
                                     text='All report',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#214312',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.all_results_btn.bind("<Button-1>", self.generate_all_report)
        self.all_results_btn.place(x=300, y=200)

    def generate_report(self, event):
        self.results_btn.unbind("<Button-1>")
        Results().get_result_current_day()
        tkMessageBox.showinfo("Updated", "Report was generated successful")
        self.results_btn.bind("<Button-1>", self.generate_report)

    def generate_all_report(self, event):
        self.all_results_btn.unbind("<Button-1>")
        Results().get_all_result()
        tkMessageBox.showinfo("Updated", "Report was generated successful")
        self.all_results_btn.bind("<Button-1>", self.generate_all_report)
