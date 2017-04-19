import Tkinter as tk
import tkMessageBox
from ConfigParser import SafeConfigParser, RawConfigParser


class SettingsView:
    def __init__(self, root, frames):
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['settings'] = self.body

        self.body.place(x=120, y=0, width=380, height=500)

        tk.Label(self.body, text='Login ').grid(row=0, column=0, columnspan=2, pady=5)
        self.email_entry = tk.Entry(self.body, width=50)
        self.email_entry.grid(row=0, column=3, columnspan=7)

        tk.Label(self.body, text='Password ').grid(row=1, column=0, columnspan=2, pady=5)
        self.pass_entry = tk.Entry(self.body, width=50)
        self.pass_entry.grid(row=1, column=3, columnspan=7)

        tk.Label(self.body, text='Search URL ').grid(row=2, column=0, columnspan=2, pady=5)
        self.url_entry = tk.Entry(self.body, width=50)
        self.url_entry.grid(row=2, column=3, columnspan=7)

        tk.Label(self.body, text='Limit ').grid(row=3, column=0, columnspan=2, pady=5)
        self.limit_entry = tk.Entry(self.body, width=50)
        self.limit_entry.grid(row=3, column=3, columnspan=7)

        self.results_btn = tk.Button(self.body,
                                     text='Update info',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.results_btn.bind("<Button-1>", self.update_settings)
        self.results_btn.place(x=130, y=450)

        config = RawConfigParser()
        config.read('../config.ini')
        self.email_entry.insert(0, config.get('main', 'email'))
        self.pass_entry.insert(0, config.get('main', 'password'))
        self.url_entry.insert(0, config.get('main', 'search_link'))
        self.limit_entry.insert(0, config.get('main', 'day_limit'))

    def update_settings(self, event):
        config = RawConfigParser()
        config.read('../config.ini')
        config.set('main', 'email', str(self.email_entry.get()))
        config.set('main', 'password', str(self.pass_entry.get()))
        config.set('main', 'search_link', str(self.url_entry.get()))
        config.set('main', 'day_limit', str(self.limit_entry.get()))

        with open('../config.ini', 'w') as f:
            config.write(f)

        tkMessageBox.showinfo("Updated", "Info update successful")
