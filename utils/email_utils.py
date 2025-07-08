import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_bulk_emails(subject, message, sender_email, sender_password, recipient_list):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for recipient in recipient_list:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))
            server.send_message(msg)

        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False
