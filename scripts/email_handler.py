import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))


if not os.path.exists("data"):
    os.makedirs("data")


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
EMAIL_ADDRESS = "youremail@gmail.com"
EMAIL_PASSWORD = "your-app-password"  


def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())


def receive_emails():
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")
        _, search_data = mail.search(None, 'ALL')
        for num in search_data[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            _, msg_data = data[0]
            msg = email.message_from_bytes(msg_data)
            subject = email.header.decode_header(msg["subject"])[0][0]
            from_ = msg.get("From")
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        save_email(num.decode(), subject, from_, body)
            else:
                body = msg.get_payload(decode=True).decode()
                save_email(num.decode(), subject, from_, body)

def save_email(num, subject, from_, body):
    file_path = os.path.join("data", f"email_{num}.txt")
    with open(file_path, "w") as f:
        f.write(f"Subject: {subject}\nFrom: {from_}\nBody:\n{body}\n")

# Example usage
if __name__ == "__main__":
    send_email("Test Subject", "This is a test email body.", "yousafzaihamza3@gmail.com")
    receive_emails()
