import pandas as pd
import os
from datetime import datetime
from tkinter import Tk, filedialog
from docx import Document
import PyPDF2
import argparse
import logging
import json  # Added for JSON support
import time

# Configure logging
logging.basicConfig(filename='doc_logger.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

LOG_PATH = 'doc_log.xlsx'


def format_date(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")


# Enhanced error handling for all file read functions
def read_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        logging.info(f"Successfully read .txt file: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
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


# Function to read CSV files
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        content = df.to_string(index=False).splitlines()
        logging.info(f"Successfully read .csv file: {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading .csv file: {e}")
        return None


# Function to read JSON files
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        content = json.dumps(data, indent=4).splitlines()
        logging.info(f"Successfully read .json file: {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading .json file: {e}")
        return None


# Function to handle the file upload through a GUI
def file_upload_gui():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select file",
                                           filetypes=[("Text files", "*.txt"),
                                                      ("Word files", "*.docx"),
                                                      ("PDF files", "*.pdf"),
                                                      ("CSV files", "*.csv"),
                                                      ("JSON files",
                                                       "*.json")])

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
    elif file_extension == '.csv':
        return read_csv(file_path)
    elif file_extension == '.json':
        return read_json(file_path)
    else:
        logging.error(f"Unsupported file format: {file_extension}")
        print(f"Unsupported file format: {file_extension}")
        return None


def log_document(file_path):
    """
    Logs content of the specified document to an Excel file.

    Parameters:
    file_path (str): Path to the document to be logged.

    Returns:
    None
    """
    # Validate file path and type
    if not os.path.isfile(file_path):
        print("Error: File does not exist.")
        return
    file_name = os.path.basename(file_path)
    # Get file size
    file_size = os.path.getsize(file_path)
    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    document_id = f"{file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Add logging of metadata
    metadata = {
        "Document Name": file_name,
        "File Size": file_size,
        "File Type": file_extension,
        "Document ID": document_id,
        "Timestamp": datetime.now()
    }
    logging.info(f"Document Metadata: {metadata}")


def export_metadata_to_json(file_metadata, json_filename="metadata.json"):
    """
    Exports file metadata to a JSON file.

    Parameters:
    file_metadata (dict): Metadata dictionary to be saved.
    json_filename (str): Name of the JSON file to save metadata.
    """
    try:
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(file_metadata, json_file, indent=4)
        logging.info(f"Metadata exported to {json_filename}")
    except Exception as e:
        logging.error(f"Error exporting metadata to JSON: {e}")


def preview_parsed_content(parsed_data, preview_length=5):
    """
    Display a preview of the parsed content.

    Parameters:
    parsed_data (list): List of parsed document lines.
    preview_length (int): Number of lines to preview.
    """
    preview = '\n'.join(parsed_data[:preview_length])
    print(f"Preview of the parsed content:\n{preview}\n")
    return preview


def read_txt_with_retry(file_path, retries=3, delay=2):
    for attempt in range(retries):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
            logging.info(f"Successfully read .txt file: {file_path}")
            return content
        except Exception as e:
            logging.error(f"Error reading .txt file \
            on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                logging.error(f"Failed to read .txt file after \
                {retries} attempts.")
                return None


# Function to log parsed data to Excel
def log_to_excel(parsed_data, file_name, log_path='doc_log.xlsx',
                 sheet_name='Documents'):
    """
    Appends data to the existing Excel log file or
    creates a new one if it doesn't exist.

    Parameters:
    parsed_data (list): List of parsed document lines to be logged.
    file_name (str): The name of the file being logged.
    log_path (str): The path of the Excel log file. Default is 'doc_log.xlsx'.
    sheet_name (str): The sheet name in the Excel file. Default is 'Documents'.

    Returns:
    None
    """
    try:
        # Create the new data to log
        data = [{'Section': f'Section {i+1}', 'Content': line.strip(),
                 'Document Name': file_name, 'Timestamp': datetime.now()}
                for i, line in enumerate(parsed_data)]

        df = pd.DataFrame(data)

        # Check if the document is already logged
        if os.path.exists(log_path):
            existing_df = pd.read_excel(log_path)
            if file_name in existing_df['Document Name'].values:
                print(f"{file_name} is already logged in {log_path}.")
                return  # Skip logging if already present

        # Backup the existing file if it exists
        if os.path.exists(log_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"backup_{timestamp}_{log_path}"
            os.rename(log_path, backup_path)
            logging.info(f"Backup saved as {backup_path}")

        # Append data to Excel
        with pd.ExcelWriter(log_path, mode='a', engine='openpyxl',
                            if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False,
                        header=not writer.sheets)

        logging.info(f"Successfully logged data from \
                     {file_name} to {log_path} in {sheet_name} sheet")
        print(f"Data successfully written to {log_path} in {sheet_name} sheet")

    except Exception as e:
        # Log error data in the 'Errors' sheet
        error_data = [{'Error Message': str(e), 'Document Name': file_name,
                       'Timestamp': datetime.now()}]
        error_df = pd.DataFrame(error_data)

        # Log error data in the 'Errors' sheet
        with pd.ExcelWriter(log_path, mode='a', engine='openpyxl',
                            if_sheet_exists='overlay') as writer:
            error_df.to_excel(writer, sheet_name='Errors', index=False,
                              header=not writer.sheets)

        logging.error(f"Error writing to Excel at {log_path}: {e}")
        print(f"Error writing to Excel: {e}")


# Main function to handle the process
def main():
    parser = argparse.ArgumentParser(description="Document Logger - \
                                     Uploads file content to an Excel log.")
    parser.add_argument('--file', type=str,
                        help='Path to the file to be logged')

    args = parser.parse_args()

    if args.file:
        file_path = args.file
        logging.info(f"CLI file upload: {file_path}")
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            print(f"File not found: {file_path}")
            return
    else:
        file_path = file_upload_gui()
        if not file_path:
            return

    parsed_data = parse_document(file_path)
    if parsed_data:
        file_name = os.path.basename(file_path)
        log_to_excel(parsed_data, file_name)


# Function to generate a summary report
def generate_summary_report(output_format='txt'):
    try:
        # Read the existing Excel log
        df = pd.read_excel('doc_log.xlsx')

        # Group by document name and file type to get some stats
        doc_summary = df.groupby('Document Name').agg({
            'Content': 'count',
            'Timestamp': 'max'
        }).reset_index()

        num_docs = len(doc_summary)
        total_lines = df['Content'].count()

        # Create summary report
        summary = "Summary Report:\n\n"
        summary += f"Total Documents Processed: {num_docs}\n"
        summary += f"Total Lines Logged: {total_lines}\n\n"
        summary += "Document Details:\n"

        for index, row in doc_summary.iterrows():
            summary += f"Document: {row['Document Name']}, \
            Lines: {row['Content']}, Last Updated: {row['Timestamp']}\n"

        # Save the summary to a text file
        with open('summary_report.txt', 'w') as file:
            file.write(summary)

        print("Summary report generated and saved as 'summary_report.txt'")

    except Exception as e:
        print(f"Error generating summary report: {e}")

    except Exception as e:
        print(f"Error generating summary report: {e}")

    # Save the summary based on the specified format
    if output_format == 'csv':
        doc_summary.to_csv('summary_report.csv', index=False)
        print("Summary report generated and saved as 'summary_report.csv'")
    else:
        with open('summary_report.txt', 'w') as file:
            file.write(summary)
        print("Summary report generated and saved as 'summary_report.txt'")


def parse_args():
    parser = argparse.ArgumentParser(description="Excel Logger")
    parser.add_argument("file_path", type=str,
                        help="Path to the document to be logged")
    parser.add_argument("--generate-summary", action="store_true",
                        help="Generate summary report after logging")
    return parser.parse_args()


args = parse_args()


if __name__ == "__main__":
    log_document(args.file_path)
    if args.generate_summary:
        generate_summary_report()
