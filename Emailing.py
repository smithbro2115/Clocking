import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def email_invoice(name, invoice_path, email_template):
    recipients, subject, body = get_email_settings_from_text(email_template)
    subject, body = replace_short_codes(subject, name), replace_short_codes(body, name)
    session = make_session()
    for recipient in recipients:
        msg = make_message(recipient, subject, body)
        attach_invoice_to_msg(invoice_path, msg)
        session.send_message(msg)
        del msg


def make_session():
    s = smtplib.SMTP(host="smtp.gmail.com", port=587)
    s.starttls()
    s.login("clocking.invoices@gmail.com", 'Ferrari578')
    return s


def make_message(recipient, subject, body):
    m = MIMEMultipart()
    m['From'] = "clocking.invoices@gmail.com"
    m["To"] = recipient
    m["Subject"] = subject
    m.attach(MIMEText(body, 'plain'))
    return m


def attach_invoice_to_msg(invoice_path, msg):
    with open(invoice_path, 'rb') as f:
        part = MIMEBase('application', 'vnd.ms-excel')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    file_name = os.path.basename(invoice_path)
    part.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(part)


def get_email_settings_from_text(text: str):
    recipients = text[text.find('@recipients\n')+len('@recipients\n'):text.find('\n\n@subject')].split(", ")
    subject = text[text.find("@subject\n")+len("@subject\n"):text.find("\n\n@body")]
    body = text[text.find("@body\n")+len("@body\n"):]
    return recipients, subject, body


def replace_short_codes(text, name):
    date = datetime.now()
    date = f"{date.strftime('%B')} {date.day}, {date.year}"
    return text.replace('[name]', name).replace('[date]', date)


