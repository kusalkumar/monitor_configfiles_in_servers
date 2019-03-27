#send_mail.py
import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#project specific imports
import paramiko_params as pp
import shared_module


class send_email:
    def __init__(self, connection_in_str, filename):
        self.port = pp.port
        self.smtp_server = pp.smtp_server
        self.sender_email = pp.sender_email
        self.receiver_email = shared_module.get_config_var('user_mail')
        self.password = pp.password
        self.filename = filename
        self.connection_in_str = connection_in_str

    def send_mail_alert(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            print("-----")
            message_content = self.get_message()
            server.sendmail(self.sender_email, self.receiver_email, message_content)
            print("sent successfully")

    def get_message(self):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        subject = "change in content of config file %s" %str(self.filename)
        message["Subject"] = subject
        #message["Bcc"] = receiver_email  # Recommended for mass emails
        body = "There is modification in config file for below server %s" %(self.connection_in_str)
        message.attach(MIMEText(body, "plain"))

        with open(self.filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {self.filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        message = message.as_string()

        return message


