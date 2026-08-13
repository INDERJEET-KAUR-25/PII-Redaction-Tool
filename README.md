# Hybrid PII Redaction Tool

A Python-based tool for automatically detecting and replacing Personally Identifiable Information (PII) from Microsoft Word (.docx) documents.

The project combines **regex-based pattern matching** with **Microsoft Presidio NLP** to accurately detect sensitive information and replace it with realistic fake values while preserving the original document structure.

---

## Features

- Detects multiple PII types
- Replaces detected PII with realistic fake data
- Preserves document formatting
- Supports paragraphs and tables
- Consistent replacements throughout the document
- Hybrid detection using Regex + NLP

---

## Supported PII Types

- Full Names
- Email Addresses
- Phone Numbers
- Company Names
- Physical Addresses
- Social Security Numbers (SSN)
- Credit Card Numbers
- Dates of Birth
- IP Addresses

---

## Project Structure

```
PII-Redaction-Tool/

│
├── input/
├── output/
├── src/
│   ├── main.py
│   ├── detector.py
│   ├── anonymizer.py
│   ├── constants.py
│   ├── config.py
│   ├── document_processor.py
│   └── utils.py
│
├── evaluation/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Detection Strategy

The tool uses a hybrid detection pipeline.

### 1. Regex Detection

Used for structured identifiers including:

- Email
- Phone
- SSN
- Credit Card
- IP Address
- Date of Birth
- Postal Address
- Company Name

### 2. NLP Detection

Microsoft Presidio with spaCy identifies contextual entities such as:

- Person Names
- Organizations
- Locations

The outputs from both detectors are merged and duplicate detections are removed before anonymization.

---

## Anonymization Strategy

The tool generates realistic fake replacements using the Faker library.

Each original value is mapped to a single fake value to ensure consistency throughout the document.

Example:

John Smith → Rahul Verma

john@gmail.com → aman123@example.com

+91 9876543210 → +91 9234567810

---

## Libraries Used

- Python
- python-docx
- Faker
- Microsoft Presidio
- spaCy
- Regex
- pandas
- scikit-learn

---

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## Run

```bash
python src/main.py
```

The processed document will be generated inside the `output` folder.

---

## Evaluation

The system is evaluated using manually annotated ground truth.

Metrics include:

- Precision
- Recall
- Accuracy
- F1 Score

---

## Future Improvements

- OCR support for scanned PDFs
- Multilingual PII detection
- Custom entity recognizers
- Confidence threshold tuning
- Web interface using Flask/FastAPI
