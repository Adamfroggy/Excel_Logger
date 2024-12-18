import unittest
from unittest.mock import patch
from datetime import datetime
import pandas as pd
from main import log_to_excel, read_csv, read_txt
import os
import threading


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


class TestLargeFileHandling(unittest.TestCase):
    def test_read_large_txt(self):
        # Creating a large test file
        with open('large_test.txt', 'w') as f:
            f.write("A" * 10**6)  # 1MB of 'A's

        result = read_txt('large_test.txt')
        # Should return a result without memory issues
        self.assertIsNotNone(result)
        os.remove('large_test.txt')  # Clean up

    def test_read_large_csv(self):
        # Creating a large test CSV file
        large_csv = pd.DataFrame({'Column1': ['A']*10**6,
                                  'Column2': ['B']*10**6})
        large_csv.to_csv('large_test.csv',
                         index=False)

        result = read_csv('large_test.csv')
        self.assertIsNotNone(result)  # Should handle large CSV without issue
        os.remove('large_test.csv')  # Clean up


class TestCorruptedFileHandling(unittest.TestCase):
    def test_read_corrupted_txt(self):
        # Simulate corrupted file by writing an incomplete file
        with open('corrupted.txt', 'w') as f:
            # Incomplete or malformed content
            f.write("This file is corrupted...")

        result = read_txt('corrupted.txt')
        self.assertIsNone(result)  # Should return None or handle the exception

        os.remove('corrupted.txt')  # Clean up

    def test_read_corrupted_csv(self):
        # Simulate a corrupted CSV file
        with open('corrupted.csv', 'w') as f:
            f.write("Col1,Col2\nA,B\nC")  # Missing data in row

        result = read_csv('corrupted.csv')
        self.assertIsNone(result)  # Should return None or handle the exception

        os.remove('corrupted.csv')  # Clean up


class TestConcurrentLogging(unittest.TestCase):

    def log_data_concurrently(self, data, file_name):
        log_to_excel(data, file_name)

    def test_concurrent_logging(self):
        # Define test data and file names
        data1 = ["Test content 1."]
        data2 = ["Test content 2."]
        file_name1 = 'concurrent_file1.txt'
        file_name2 = 'concurrent_file2.txt'

        # Start threads for concurrent logging
        thread1 = threading.Thread(target=self.log_data_concurrently,
                                   args=(data1, file_name1))
        thread2 = threading.Thread(target=self.log_data_concurrently,
                                   args=(data2, file_name2))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Validate the log file contents
        logged_data = pd.read_excel('doc_log.xlsx')
        self.assertIn(file_name1, logged_data['Document Name'].values)
        self.assertIn(file_name2, logged_data['Document Name'].values)
        self.assertIn("Test content 1.", logged_data['Content'].values)
        self.assertIn("Test content 2.", logged_data['Content'].values)


if __name__ == '__main__':
    unittest.main()
