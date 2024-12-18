import pandas as pd
import logging


def read_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()  # Return the file contents as a string
    except Exception as e:
        logging.error(f"Error reading text file {file_path}: {e}")
        return None


def read_csv(file_path):
    try:
        return pd.read_csv(file_path)  # Uses pandas to read the CSV
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
        return None
