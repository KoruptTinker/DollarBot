import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class GMailClient:
    _email_address: str = ""
    _password: str = ""

    def __init__(self, email: str = "", password: str = ""):
        self._email_address = email
        self._password = password

    def send_email(
        self,
        to_email: str = "",
        subject: str = "",
        content: str = "",
        attachment: str = "",
    ):
        sender_address = self._email_address
        sender_pass = self._password
        receiver_address = to_email
        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = receiver_address
        message["Subject"] = subject
        # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(content, "plain"))
        if attachment != "":
            attach_file_name = attachment
            attach_file = open(attach_file_name, "rb")
            payload = MIMEBase("application", "octet-stream")
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)  # encode the attachment
            # add payload header with filename
            payload.add_header(
                "Content-Disposition", f"attachment; filename={attach_file_name}"
            )
            message.attach(payload)
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
