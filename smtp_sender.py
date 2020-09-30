import smtplib
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import sys, os

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


def attach_file(msg, filepath):
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        with open(filepath) as fp:
            file = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
    else:
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)


# TODO: test and make work with different smtp servers!
def send_smtp_email(body_text, filepath=None):
    try:
        host = servername
        from_addr = user

        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["Subject"] = "DOCUMENTATION NOTIFY"
        msg["Date"] = formatdate(localtime=True)

        if body_text:
            msg.attach(MIMEText(body_text))

        to_list = []
        for el in to_email.split(";"):
            if el.strip() != "":
                to_list.append(el.strip())

        msg["To"] = ', '.join(to_list)

        if filepath:
            if os.path.isfile(filepath):
                attach_file(msg, filepath)

        emails = to_list
        server = smtplib.SMTP(host)
        server.login(user, password)
        server.sendmail(user, emails, msg.as_string())
        server.quit()
    except BaseException as ex:
        sys.stderr.write("EXCEPTION: " + str(ex) + "\n")
