import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Make src importable
sys.path.append("src")

from document_processor import DocumentProcessor
from detector import HybridDetector
from anonymizer import FakeDataReplacer

st.set_page_config(page_title="PII Redaction Tool")

st.title("PII Redaction Tool")
st.write("Upload a DOCX file to detect and anonymize PII.")

uploaded_file = st.file_uploader(
    "Choose a DOCX file",
    type=["docx"]
)

if uploaded_file is not None:

    with tempfile.TemporaryDirectory() as tmpdir:

        input_path = os.path.join(tmpdir, "input.docx")
        output_path = os.path.join(tmpdir, "redacted.docx")

        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        processor = DocumentProcessor(input_path)
        detector = HybridDetector()
        replacer = FakeDataReplacer()

        # Paragraphs
        for paragraph in processor.get_paragraphs():

            text = paragraph.text

            if not text.strip():
                continue

            entities = detector.detect(text)

            if entities:
                paragraph.text = replacer.replace(text, entities)

        # Tables
        for table in processor.get_tables():

            for row in table.rows:

                for cell in row.cells:

                    text = cell.text

                    if not text.strip():
                        continue

                    entities = detector.detect(text)

                    if entities:
                        cell.text = replacer.replace(text, entities)

        processor.save(output_path)

        with open(output_path, "rb") as file:

            st.success("Redaction completed successfully!")

            st.download_button(
                label="Download Redacted Document",
                data=file,
                file_name="Redacted.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )