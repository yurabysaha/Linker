import Tkinter as tk
import threading
import tkMessageBox
from ConfigParser import RawConfigParser
from user import User
from connect import Connect
from sales_tool import Sales


class ConnectView:
    def __init__(self, root, frames, textfield):

        self.text = textfield
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['connect'] = self.body
        self.body.place(x=0, y=340, width=700, height=260)
        data = User().count_connections()
        self.count_today = data[0][0]
        self.count_all = data[1][0]
        tk.Label(self.body, bg='#e6e6e6', text='Today     |     All ').place(x=410, y=100)
        tk.Label(self.body, bg='#e6e6e6', text='Send requests  ').place(x=420, y=70)
        self.counts = tk.Label(self.body, bg='#e6e6e6', text=' %s     |     %s ' % (self.count_today, self.count_all))
        self.counts.place(x=422, y=120)

        tk.Label(self.body, bg='#e6e6e6', text='Message Text For Sales Connect').place(x=1, y=1)
        self.sales_mess_entry = tk.Text(self.body, width=38, height=13)
        self.sales_mess_entry.place(x=10, y=24)

        config = RawConfigParser()
        config.read('../config.ini')
        self.sales_mess_entry.insert(1.0, config.get('main', 'sales_message_text'))

        self.update_mess_btn = tk.Button(self.body,
                                         text='Update info',
                                         fg='#ffffff',
                                         bg='#214312', activebackground='#e6e6e6',
                                         borderwidth=0,
                                         highlightthickness=0,
                                         width=13, height=2)

        self.update_mess_btn.bind("<Button-1>", self.update_message_text)
        self.update_mess_btn.place(x=330, y=24)

        self.connect_btn = tk.Button(self.body,
                                     text='Start Simple Connect',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=17, height=2)

        self.connect_btn.bind("<Button-1>", self.start_connect)
        self.connect_btn.place(x=330, y=200)

        self.sales_connect_btn = tk.Button(self.body,
                                     text='Start Sales Connect',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=17, height=2)

        self.sales_connect_btn.bind("<Button-1>", self.start_sales_connect)
        self.sales_connect_btn.place(x=460, y=200)

    def start_connect(self, event):
            self.connect_btn.unbind("<Button 1>")
            self.connect_btn.config(state='disabled')
            t = threading.Thread(target=Connect, args=(self.text, self))
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

    def counts_update(self):
        self.count_today += 1
        self.count_all += 1
        self.counts.config(text=' %s     |     %s ' % (self.count_today, self.count_all))
