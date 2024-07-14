import os
import re
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

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

def preprocess_all_emails(data_dir):
    """
    Preprocess all emails in the given directory.
    Save the preprocessed text to new files prefixed with 'preprocessed_'.
    """
    for filename in os.listdir(data_dir):
        if filename.startswith("email_") and filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r") as f:
                text = f.read()
                preprocessed_text = preprocess_email(text)
                preprocessed_file_path = os.path.join(data_dir, f"preprocessed_{filename}")
                with open(preprocessed_file_path, "w") as out_f:
                    out_f.write(preprocessed_text)

if __name__ == "__main__":
    preprocess_all_emails("data")
