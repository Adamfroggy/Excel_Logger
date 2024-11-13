import unittest
from unittest.mock import patch
from datetime import datetime
import pandas as pd
from main import log_to_excel


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


if __name__ == '__main__':
    unittest.main()
