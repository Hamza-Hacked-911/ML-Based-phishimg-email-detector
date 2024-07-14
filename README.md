# Email Phishing Detector

This project is an automated email phishing detector that continuously monitors an email inbox for new emails, processes them to detect phishing attempts, and moves detected phishing emails to a specific folder.

## Features

- Preprocesses email text using SpaCy
- Uses TF-IDF vectorization for feature extraction
- Trains a Stochastic Gradient Descent (SGD) Classifier to detect phishing emails
- Automatically detects and handles new emails

## Requirements

- Python 3.x
- SpaCy
- Scikit-learn
- Joblib
- Imaplib
- Email

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Hamza-Hacked-911/ML-Based-phishimg-email-detector.git
   cd ML-Based-phishimg-email-detector/scripts
