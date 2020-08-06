import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import sys

to_email = "addr to send notifications"
user = "smtp username"
password = "smtp user password"
servername = "servername or ip"


def set_smtp_settings(us, psw, host, addrto):
    global user, password, servername, to_email
    user = us
    password = psw
    servername = host
    to_email = addrto


def send_smtp_email(body_text):
    try:
        host = servername
        from_addr = user

        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["Subject"] = "DOCUMENTATION NOTIFY"
        msg["Date"] = formatdate(localtime=True)

        if body_text:
            msg.attach(MIMEText(body_text))

        msg["To"] = to_email

        emails = [to_email]
        server = smtplib.SMTP(host)
        server.login(user, password)
        server.sendmail(user, emails, msg.as_string())
        server.quit()
    except BaseException as ex:
        sys.stderr.write("EXCEPTION: " + str(ex) + "\n")
