import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class GMailClient:
    """A client for sending emails through Gmail's SMTP server.

    This class provides functionality to send emails with optional attachments
    using Gmail's SMTP server. It handles the connection, authentication, and
    message composition.
    """

    _email_address: str = ""
    _password: str = ""

    def __init__(self, email: str = "", password: str = ""):
        """Initialize the Gmail client with credentials."""
        self._email_address = email
        self._password = password

    def send_email(
        self,
        to_email: str = "",
        subject: str = "",
        content: str = "",
        attachment: str = "",
    ):
        """Send an email through Gmail's SMTP server.

        Sends an email with optional attachment using the configured Gmail account.
        Uses TLS encryption for secure communication.

        Args:
            to_email (str, optional): Recipient's email address. Defaults to empty string.
            subject (str, optional): Email subject line. Defaults to empty string.
            content (str, optional): Plain text content of email. Defaults to empty string.
            attachment (str, optional): Path to file to attach. Defaults to empty string.

        The function:
            1. Creates a MIME multipart message
            2. Attaches the text content and optional file
            3. Establishes secure SMTP connection
            4. Sends the email and closes the connection
        """
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
