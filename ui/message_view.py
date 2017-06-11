import Tkinter as tk
import threading
import tkMessageBox
from user import User
from ConfigParser import RawConfigParser
from message import Message


class MessageView:
    def __init__(self, root, frames, text):
        self.text = text
        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['message'] = self.body
        frames['message'].place(x=0, y=340, width=700, height=260)

        tk.Label(self.body, bg='#e6e6e6', text='Message Text').place(x=1, y=1)
        self.mess_entry = tk.Text(self.body, width=38, height=13)
        self.mess_entry.place(x=10, y=24)

        self.update_mess_btn = tk.Button(self.body,
                                         text='Update info',
                                         fg='#ffffff',
                                         bg='#214312', activebackground='#e6e6e6',
                                         borderwidth=0,
                                         highlightthickness=0,
                                         width=13, height=2)

        self.update_mess_btn.bind("<Button-1>", self.update_message_text)
        self.update_mess_btn.place(x=330, y=24)

        self.send_mess_btn = tk.Button(self.body,
                                     text='Send messages',
                                     fg='#ffffff',
                                     bg='#214312', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.send_mess_btn.bind("<Button-1>", self.send_message)
        self.send_mess_btn.place(x=390, y=200)

        config = RawConfigParser()
        config.read('../config.ini')
        self.mess_entry.insert(1.0, config.get('main', 'message_text'))

        data = User().candidate_for_message()
        self.count_message = len(data)
        self.count_label = tk.Label(self.body, bg='#e6e6e6', text='Candidate for message: %s' % self.count_message)
        self.count_label.place(x=330, y=70)

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
        t = threading.Thread(target=Message, args=(self.text, self))
        t.start()
        self.text.insert('end', "Start send messages\n")

    def update_count(self):
        self.count_message -= 1
        self.count_label.config(text='Candidate for message: %s' % self.count_message)

    def update_count_from_db(self):
        data = User().candidate_for_message()
        self.count_message = len(data)
        self.count_label.config(text='Candidate for message: %s' % self.count_message)
