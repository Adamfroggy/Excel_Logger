import pandas as pd


def read_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()  # Return the file contents as a string
    except Exception as e:
        print(f"Error reading text file {file_path}: {e}")
        return None


def read_csv(file_path):
    try:
        # Uses pandas to read the CSV into a DataFrame
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return None
