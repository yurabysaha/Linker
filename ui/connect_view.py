import Tkinter as tk
import threading
import user

from connect import Connect


class ConnectView:
    def __init__(self, root, frames, textfield):

        self.text = textfield
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['connect'] = self.body
        self.body.place(x=120, y=0, width=380, height=500)
        data = user.count_connections()
        tk.Label(self.body, text='Today   |   All ').place(x=130, y=10)
        tk.Label(self.body, text='Send requests:  ').place(x=10, y=30)
        tk.Label(self.body, text=' %s | %s ' % (data[0][0], data[1][0])).place(x=154, y=30)
        self.connect_btn = tk.Button(self.body,
                                     text='Start connect',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.connect_btn.bind("<Button-1>", self.start_connect)
        self.connect_btn.place(x=130, y=450)

    def start_connect(self, event):
            self.connect_btn.unbind("<Button 1>")
            self.connect_btn.config(state='disabled')
            t = threading.Thread(target=Connect, args=(self.text,))
            t.start()
            self.text.insert('end', "Start connect people\n")
