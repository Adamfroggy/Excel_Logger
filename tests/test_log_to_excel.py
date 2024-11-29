import unittest
from unittest.mock import patch
from datetime import datetime
import pandas as pd
from main import log_to_excel
import os


class TestLogToExcel(unittest.TestCase):

    @patch('main.pd.DataFrame')  # Mock the DataFrame constructor
    @patch('main.os.path.exists')  # Mock os.path.exists
    @patch('main.pd.ExcelWriter')  # Mock ExcelWriter
    def test_log_to_excel(self, mock_writer, mock_exists, mock_df):
        parsed_data = ['Line 1', 'Line 2']
        file_name = 'test_document.txt'
        log_path = 'test_log.xlsx'

        mock_exists.return_value = True
        mock_df.return_value = pd.DataFrame([{'Section': 'Section 1',
                                              'Content': 'Line 1'}])

        log_to_excel(parsed_data, file_name, log_path=log_path,
                     sheet_name='Documents')

        mock_writer.assert_called_with(log_path, mode='a', engine='openpyxl',
                                       if_sheet_exists='overlay')
        mock_df.assert_called_with([{'Section': 'Section 1',
                                     'Content': 'Line 1', 'Document Name':
                                     'test_document.txt',
                                     'Timestamp': datetime.now()}])


class TestInvalidExcelLogging(unittest.TestCase):
    def test_invalid_data_format(self):
        # Passing a dictionary instead of expected format
        # (e.g., list or DataFrame)
        invalid_data = {'key': 'value'}
        # Assuming ValueError is raised for invalid data
        with self.assertRaises(ValueError):
            log_to_excel(invalid_data, 'invalid_file.txt')

    def test_invalid_column_names(self):
        # Mock data with invalid column names for Excel logging
        invalid_data = pd.DataFrame({'InvalidCol': ['Test']})
        # Assuming a KeyError if specific columns are missing
        with self.assertRaises(KeyError):
            log_to_excel(invalid_data)


class TestExcelFileOpen(unittest.TestCase):
    def test_excel_file_open(self):
        # Simulating the case when the Excel file
        # is open in another application
        with open('doc_log.xlsx', 'w') as f:
            f.write("Test")  # Writing to the file to simulate it being open

        data = ["Test content."]
        try:
            # Attempt to log data while the file is open
            log_to_excel(data, 'test_open_file.txt')
            # File should still exist
            self.assertTrue(os.path.exists('doc_log.xlsx'))
        except PermissionError:
            self.fail("PermissionError: Excel file is open. \
                      Logging should handle this gracefully.")


if __name__ == '__main__':
    unittest.main()
