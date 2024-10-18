import pandas as pd
import os
from datetime import datetime
from tkinter import Tk, filedialog
from docx import Document


# Function to read text files
def read_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        return content
    except Exception as e:
        print(f"Error reading .txt file: {e}")
        return None


# Function to read .docx files
def read_docx(file_path):
    try:
        doc = Document(file_path)
        content = [para.text for para in doc.paragraphs if para.text.strip()]
        return content
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return None


# Function to handle the file upload
def file_upload():
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    file_path = filedialog.askopenfilename(title="Select file",
                                           filetypes=[("Text files", "*.txt"),
                                                      ("Word files",
                                                       "*.docx")])

    if not file_path:
        print("No file selected. Exiting.")
        return None

    print(f"File selected: {file_path}")
    return file_path


# Function to parse the document
def parse_document(file_path):
    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.txt':
        return read_txt(file_path)
    elif file_extension == '.docx':
        return read_docx(file_path)
    else:
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

        print("Data successfully written to doc_log.xlsx")
    except Exception as e:
        print(f"Error writing to Excel: {e}")


# Main function to handle the process
def main():
    file_path = file_upload()
    if not file_path:
        return

    parsed_data = parse_document(file_path)
    if not parsed_data:
        return

    file_name = os.path.basename(file_path)
    log_to_excel(parsed_data, file_name)


if __name__ == '__main__':
    main()
