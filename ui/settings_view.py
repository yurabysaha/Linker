import Tkinter as tk


class SettingsView:
    def __init__(self, root, frames):
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['settings'] = self.body

        self.body.place(x=120, y=0, width=380, height=435)

        tk.Label(self.body, text='Login ').grid(row=0, column=0, columnspan=2, pady=5)
        self.mutal_entry = tk.Entry(self.body, width=50)
        self.mutal_entry.grid(row=0, column=3, columnspan=7)

        tk.Label(self.body, text='Password ').grid(row=1, column=0, columnspan=2, pady=5)
        self.mutal_entry = tk.Entry(self.body, width=50)
        self.mutal_entry.grid(row=1, column=3, columnspan=7)
