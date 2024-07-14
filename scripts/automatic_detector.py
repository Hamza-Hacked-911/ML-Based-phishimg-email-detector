import time
import imaplib
import email
import os
import re
import joblib
import spacy
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sklearn.feature_extraction.text import TfidfVectorizer

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")


model = joblib.load("../models/phishing_detection_model.pkl")
vectorizer = joblib.load("../models/vectorizer.pkl")


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
EMAIL_ADDRESS = "youremail@gmail.com"
EMAIL_PASSWORD = "your-app-password"  

def preprocess_email(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def detect_phishing(email_text):
    preprocessed_text = preprocess_email(email_text)
    features = vectorizer.transform([preprocessed_text])
    prediction = model.predict(features)
    return prediction[0]

def move_to_folder(mail, num, folder):
    result = mail.store(num, '+X-GM-LABELS', folder)
    if result[0] == 'OK':
        mail.store(num, '+FLAGS', '\\Deleted')
        mail.expunge()

def process_emails():
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")
        
        while True:
            print("Checking for new emails...")
            status, search_data = mail.search(None, 'UNSEEN')
            
            if search_data[0]:
                print(f"Found {len(search_data[0].split())} new emails.")
            else:
                print("No new emails.")

            for num in search_data[0].split():
                status, data = mail.fetch(num, '(RFC822)')

                if status != 'OK':
                    print(f"Failed to fetch email {num.decode()}")
                    continue

                _, msg_data = data[0]
                msg = email.message_from_bytes(msg_data)
                
                sender = msg['From']
                subject = msg['Subject']
                subject, encoding = decode_header(subject)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            email_body = part.get_payload(decode=True).decode()
                            break
                else:
                    email_body = msg.get_payload(decode=True).decode()

                is_phishing = detect_phishing(email_body)
                if is_phishing:
                    move_to_folder(mail, num, "Phishing")
                    print(f"Sender: {sender}")
                    print(f"Message: {email_body[:100]}...")  
                    print("Status: Phishing\n")
                else:
                    move_to_folder(mail, num, "Legitimate")
                    print(f"Sender: {sender}")
                    print(f"Message: {email_body[:100]}...")  
                    print("Status: Legitimate\n")
            
            time.sleep(60)  

if __name__ == "__main__":
    process_emails()
