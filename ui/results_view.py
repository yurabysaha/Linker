import Tkinter as tk

from results import Results


class ResultsView:
    def __init__(self, root, frames):

        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['results'] = self.body

        frames['results'].place(x=120, y=0, width=380, height=435)
        tk.Label(self.body, text='Generate Report').place(x=102, y=2)
        self.results_btn = tk.Button(self.body,
                                     text='Today report',
                                     bg='#545424', activebackground='#545424',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.results_btn.bind("<Button-1>", self.generate_report)
        self.results_btn.place(x=20, y=30)

        self.results_btn = tk.Button(self.body,
                                     text='All report',
                                     bg='#545424', activebackground='#545424',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.results_btn.bind("<Button-1>", self.generate_all_report)
        self.results_btn.place(x=170, y=30)

    def generate_report(self, event):
            Results().get_result_current_day()
    def generate_all_report(self, event):
            Results().get_all_result()