import unittest
import pandas as pd
from main import log_to_excel, log_document, read_csv, read_txt
import os
import threading


class TestEmptyFileHandling(unittest.TestCase):
    def test_read_empty_txt(self):
        # Create an empty file
        open('empty_test.txt', 'w').close()

        result = read_txt('empty_test.txt')
        self.assertEqual(result, '')  # Expect empty string
        os.remove('empty_test.txt')  # Clean up

    def test_read_empty_csv(self):
        # Create an empty CSV file
        pd.DataFrame().to_csv('empty_test.csv', index=False)

        result = read_csv('empty_test.csv')
        self.assertTrue(result.empty)  # Expect an empty DataFrame
        os.remove('empty_test.csv')  # Clean up


class TestLoggingErrors(unittest.TestCase):
    def test_invalid_file_path(self):
        # Adjust exception type if specific error is expected
        with self.assertRaises(Exception):
            log_document('non_existent_file.txt')


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


class TestUnsupportedFileHandling(unittest.TestCase):
    def test_unsupported_file_type(self):
        # Adjust exception type if specific error is expected
        with self.assertRaises(Exception):
            log_document('unsupported_file.xyz')


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
