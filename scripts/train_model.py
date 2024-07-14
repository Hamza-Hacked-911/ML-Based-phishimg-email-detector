import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

def preprocess_email(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_preprocess_data(file_paths, sample_size=None):
    emails = []
    labels = []
    for file_path in file_paths:
        data = pd.read_csv(file_path, encoding='ISO-8859-1')
        data = data.dropna(axis=1, how='all')
        if 'label' not in data.columns:
            data.columns = ['label', 'content'] + list(data.columns[2:])
        else:
            data = data[['label', 'text']]
            data.columns = ['label', 'content']
        if sample_size:
            data = data.sample(n=sample_size)
        data['label'] = data['label'].map({'spam': 1, 'ham': 0})
        data['content'] = data['content'].apply(preprocess_email)
        emails.extend(data['content'])
        labels.extend(data['label'])
    return emails, labels

def train_model(data_dir, file_names, sample_size=None):
    file_paths = [os.path.join(data_dir, file_name) for file_name in file_names]
    emails, labels = load_and_preprocess_data(file_paths, sample_size=sample_size)
    
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(emails)
    y = labels

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    class_weights = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train)
    class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

    model = SGDClassifier(max_iter=1000, class_weight=class_weight_dict)
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    print("Training Set Evaluation")
    print(f"Accuracy: {accuracy_score(y_train, y_train_pred)}")
    print(classification_report(y_train, y_train_pred, zero_division=0))

    y_test_pred = model.predict(X_test)
    print("Test Set Evaluation")
    print(f"Accuracy: {accuracy_score(y_test, y_test_pred)}")
    print(classification_report(y_test, y_test_pred, zero_division=0))

    
    joblib.dump(model, "../models/phishing_detection_model.pkl")
    joblib.dump(vectorizer, "../models/vectorizer.pkl")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "../data")
    train_model(data_dir, ["spam.csv", "spam_ham_dataset.csv"], sample_size=2000)
