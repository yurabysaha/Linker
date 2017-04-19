import Tkinter as tk
import threading
import tkMessageBox
from ConfigParser import RawConfigParser
from message import Message


class MessageView:
    def __init__(self, root, frames, text):
        self.text = text
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['message'] = self.body

        frames['message'].place(x=120, y=0, width=380, height=500)

        tk.Label(self.body, text='Message Text ').grid(row=0, column=0, columnspan=2, pady=5)
        self.mess_entry = tk.Text(self.body, width=46, height=17)
        self.mess_entry.grid(row=1, column=1, columnspan=7)

        self.update_mess_btn = tk.Button(self.body,
                                     text='Update info',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.update_mess_btn.bind("<Button-1>", self.update_message_text)
        self.update_mess_btn.place(x=130, y=320)

        self.send_mess_btn = tk.Button(self.body,
                                     text='Send messages',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.send_mess_btn.bind("<Button-1>", self.send_message)
        self.send_mess_btn.place(x=130, y=450)

        config = RawConfigParser()
        config.read('../config.ini')
        self.mess_entry.insert(1.0, config.get('main', 'message_text'))

    def update_message_text(self, event):
        config = RawConfigParser()
        config.read('../config.ini')
        config.set('main', 'message_text', str(self.mess_entry.get(1.0, 'end')))

        with open('../config.ini', 'w') as f:
            config.write(f)

        tkMessageBox.showinfo("Updated", "Message text update successful")

    def send_message(self, event):
        self.send_mess_btn.unbind("<Button 1>")
        self.send_mess_btn.config(state='disabled')
        t = threading.Thread(target=Message, args=(self.text,))
        t.start()
        self.text.insert('end', "Start send messages\n")
