import Tkinter as tk
import threading
import tkMessageBox
from ConfigParser import RawConfigParser

import user

from connect import Connect


class ConnectView:
    def __init__(self, root, frames, textfield):

        self.text = textfield
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['connect'] = self.body
        self.body.place(x=120, y=0, width=380, height=500)
        data = user.count_connections()
        tk.Label(self.body, bg='#e6e6e6', text='Today     |     All ').place(x=130, y=10)
        tk.Label(self.body, bg='#e6e6e6', text='Send requests  ').place(x=10, y=30)
        tk.Label(self.body, bg='#e6e6e6', text=' %s     |     %s ' % (data[0][0], data[1][0])).place(x=154, y=30)

        tk.Label(self.body, bg='#e6e6e6', text='Message Text For Sales Connect').place(x=10, y=60)
        self.sales_mess_entry = tk.Text(self.body, width=46, height=14)
        self.sales_mess_entry.place(x=10, y=80)

        config = RawConfigParser()
        config.read('../config.ini')
        self.sales_mess_entry.insert(1.0, config.get('main', 'sales_message_text'))

        self.update_mess_btn = tk.Button(self.body,
                                         text='Update info',
                                         fg='#ffffff',
                                         bg='#214312', activebackground='#e6e6e6',
                                         borderwidth=0,
                                         highlightthickness=0,
                                         width=18, height=2)

        self.update_mess_btn.bind("<Button-1>", self.update_message_text)
        self.update_mess_btn.place(x=130, y=320)

        self.connect_btn = tk.Button(self.body,
                                     text='Start Simple Connect',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.connect_btn.bind("<Button-1>", self.start_connect)
        self.connect_btn.place(x=40, y=450)

        self.sales_connect_btn = tk.Button(self.body,
                                     text='Start Sales Connect',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.sales_connect_btn.bind("<Button-1>", self.start_sales_connect)
        self.sales_connect_btn.place(x=180, y=450)

    def start_connect(self, event):
            self.connect_btn.unbind("<Button 1>")
            self.connect_btn.config(state='disabled')
            t = threading.Thread(target=Connect, args=(self.text,))
            t.start()
            self.text.insert('end', "Start Simple Connect people\n")

    def start_sales_connect(self, event):
            self.connect_btn.unbind("<Button 1>")
            self.connect_btn.config(state='disabled')
            t = threading.Thread(target=Sales, args=(self.text,))
            t.start()
            self.text.insert('end', "Start Sales Connect people\n")

    def update_message_text(self, event):
        config = RawConfigParser()
        config.read('../config.ini')
        config.set('main', 'sales_message_text', str(self.sales_mess_entry.get(1.0, 'end')))

        with open('../config.ini', 'w') as f:
            config.write(f)

        tkMessageBox.showinfo("Updated", "Message text update successful")
