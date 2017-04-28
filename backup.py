import smtplib
import mimetypes
from ConfigParser import RawConfigParser
from datetime import date
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class Backup:
    def __init__(self):
        self.config = RawConfigParser()
        self.config.read('../config.ini')
        self.who = self.config.get('main', 'email')
        self.backup_date = self.config.get('main', 'backup_date')

    def send_backup_to_email(self):
        if self.backup_date != str(date.today()) or self.backup_date == '':
            email_from = "yonchibackup@gmail.com"
            email_to = "yonchibackup@gmail.com"
            file_to_send = "../db"
            username = "yonchibackup@gmail.com"
            password = "YonchiWTF"
            msg = MIMEMultipart()
            msg["From"] = email_from
            msg["To"] = email_to
            msg["Subject"] = "%s" % self.who
            ctype, encoding = mimetypes.guess_type(file_to_send)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            fp = open(file_to_send, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)

            attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)
            msg.attach(attachment)

            server = smtplib.SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(username, password)
            server.sendmail(email_from, email_to, msg.as_string())
            server.quit()
            self.backup_date = self.config.set('main', 'backup_date', str(date.today()))
            with open('../config.ini', 'w') as f:
                self.config.write(f)
