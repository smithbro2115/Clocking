import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def attach_invoice_to_msg(invoice_path, msg):
    with open(invoice_path, 'rb') as f:
        part = MIMEBase('application', 'vnd.ms-excel')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    file_name = os.path.basename(invoice_path)
    part.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(part)


def get_subject_and_body_from_text(text: str):
    subject = text[text.find("@subject\n")+len("@subject\n"):text.find("\n\n@body")]
    body = text[text.find("@body\n")+len("@body\n"):]
    return subject, body

# s = smtplib.SMTP(host="smtp.gmail.com", port=587)
# s.starttls()
# s.login("clocking.invoices@gmail.com", 'Ferrari578')
#
# m = MIMEMultipart()
# m['From'] = "clocking.invoices@gmail.com"
# m["To"] = "brinkmansound@gmail.com"
# m["Subject"] = "This is a test"
# m.attach(MIMEText("Hello this is a test", 'plain'))
#
#
# s.send_message(m)
# del m

