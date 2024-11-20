# -*- coding: utf-8 -*-
"""Web scraping and Embedding

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/170KnAshvGxRTfPCpnihf7_Yc8CYfO2BO
"""

!pip install PyMuPDF
!pip install jsonlines
from google.colab import files

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

import fitz
import jsonlines

def pdf_to_jsonl(pdf_path, jsonl_path):
  with fitz.open(pdf_path) as doc:
    with jsonlines.open(jsonl_path, mode='w') as writer:
      for page in doc:
        text = page.get_text()
        writer.write({"text": text})

pdf_path = 'foia-report-2023.pdf'
jsonl_path = 'output.jsonl'
pdf_to_jsonl(pdf_path, jsonl_path)
pdf_path
jsonl_path

CODE FOR SCRAPING THE PDFS
import os
!pip install PyPDF2
from PyPDF2 import PdfReader

# Step 1: Directory Setup
# Directory where the FCC PDFs are stored
fcc_directory = "/content/fcc"

# Ensure the directory exists
if not os.path.exists(fcc_directory):
    raise FileNotFoundError(f"The directory '{fcc_directory}' does not exist.")

# Step 2: Function to Scrape Text from All PDFs
def scrape_fcc_pdfs(directory_path):
    """
    Scrapes text from all PDF files in the specified directory.

    Args:
        directory_path (str): Path to the directory containing PDFs.

    Returns:
        dict: A dictionary where keys are filenames and values are extracted text.
    """
    pdf_texts = {}

    # Iterate through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".pdf"):  # Ensure file is a PDF
            pdf_path = os.path.join(directory_path, file_name)
            try:
                # Extract text from the PDF
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

                # Save extracted text into the dictionary
                pdf_texts[file_name] = text
                print(f"Scraped text from: {file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

    return pdf_texts

# Step 3: Run the Scraper and Store Results
fcc_texts = scrape_fcc_pdfs(fcc_directory)

# Step 4: Save Extracted Text to a File
output_file = "/content/fcc_texts.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for file_name, text in fcc_texts.items():
        f.write(f"File: {file_name}\n")
        f.write(f"Content:\n{text}\n")
        f.write("=" * 50 + "\n")  # Separator for each file

print(f"Scraped FCC texts saved to: {output_file}")



