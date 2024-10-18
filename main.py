import pandas as pd
import os
from datetime import datetime
from tkinter import Tk, filedialog
from docx import Document
import PyPDF2
import argparse
import logging  # Import logging for error and success tracking

# Configure logging
logging.basicConfig(filename='doc_logger.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Function to read text files
def read_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        logging.info(f"Successfully read .txt file: {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading .txt file: {e}")
        return None


# Function to read .docx files
def read_docx(file_path):
    try:
        doc = Document(file_path)
        content = [para.text for para in doc.paragraphs if para.text.strip()]
        logging.info(f"Successfully read .docx file: {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading .docx file: {e}")
        return None


# Function to read .pdf files
def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = [page.extract_text() for page in reader.pages
                       if page.extract_text().strip()]
        logging.info(f"Successfully read .pdf file: {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading .pdf file: {e}")
        return None


# Function to handle the file upload through a GUI
def file_upload_gui():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select file",
                                           filetypes=[("Text files", "*.txt"),
                                                      ("Word files", "*.docx"),
                                                      ("PDF files", "*.pdf")])

    if not file_path:
        logging.warning("No file selected through GUI.")
        print("No file selected. Exiting.")
        return None

    logging.info(f"File selected via GUI: {file_path}")
    return file_path


# Function to parse the document based on its extension
def parse_document(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.txt':
        return read_txt(file_path)
    elif file_extension == '.docx':
        return read_docx(file_path)
    elif file_extension == '.pdf':
        return read_pdf(file_path)
    else:
        logging.error(f"Unsupported file format: {file_extension}")
        print(f"Unsupported file format: {file_extension}")
        return None


# Function to log parsed data to Excel
def log_to_excel(parsed_data, file_name):
    try:
        data = [{'Section': f'Section {i+1}', 'Content': line.strip(),
                 'Document Name': file_name, 'Timestamp': datetime.now()}
                for i, line in enumerate(parsed_data)]

        df = pd.DataFrame(data)

        with pd.ExcelWriter('doc_log.xlsx', mode='a', engine='openpyxl',
                            if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=not writer.sheets)

        logging.info(f"Successfully logged data from {file_name} \
                     to doc_log.xlsx")
        print("Data successfully written to doc_log.xlsx")
    except Exception as e:
        logging.error(f"Error writing to Excel: {e}")
        print(f"Error writing to Excel: {e}")


# Main function to handle the process
def main():
    # Create an argument parser for CLI support
    parser = argparse.ArgumentParser(description="Document Logger - \
                                     Uploads file content to an Excel log.")
    parser.add_argument('--file', type=str,
                        help='Path to the file to be logged')

    # Parse arguments
    args = parser.parse_args()

    if args.file:
        file_path = args.file
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            print(f"File not found: {file_path}")
            return
    else:
        # If no file is provided via CLI, open GUI to select file
        file_path = file_upload_gui()
        if not file_path:
            return

    parsed_data = parse_document(file_path)
    if not parsed_data:
        return

    file_name = os.path.basename(file_path)
    log_to_excel(parsed_data, file_name)


if __name__ == '__main__':
    main()
