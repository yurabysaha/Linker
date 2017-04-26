import smtplib
import mimetypes
from ConfigParser import RawConfigParser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class Backup:
    def __init__(self, text):
        config = RawConfigParser()
        config.read('../config.ini')
        self.who = config.get('main', 'email')
        self.send_backup_to_email()

    def send_backup_to_email(self):
        emailfrom = "yonchibackup@gmail.com"
        emailto = "yonchibackup@gmail.com"
        fileToSend = "db"
        username = "yonchibackup@gmail.com"
        password = "YonchiWTF"
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "%s" % self.who
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)

        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
