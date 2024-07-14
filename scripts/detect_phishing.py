import joblib
import spacy
import re


nlp = spacy.load("en_core_web_sm")


model = joblib.load("../models/phishing_detection_model.pkl")
vectorizer = joblib.load("../models/vectorizer.pkl")

def preprocess_email(text):
    """
    Preprocess the email text using SpaCy.
    Tokenize and lemmatize the text, remove stop words and punctuation.
    """
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

# Example usage
if __name__ == "__main__":
    email_text = """
Hi Muhammad Hamza,
how are you ?
hope so u are doing great
    """
    result = detect_phishing(email_text)
    print("Phishing" if result else "Legitimate")
