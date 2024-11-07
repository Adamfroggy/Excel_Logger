import unittest
import pandas as pd
from main import read_txt, read_docx, read_pdf, read_csv, read_json, \
                log_to_excel, log_document
import os


class TestDocumentLogger(unittest.TestCase):

    def test_read_txt(self):
        result = read_txt('sample.txt')
        self.assertIsNotNone(result)

    def test_read_docx(self):
        result = read_docx('sample.docx')
        self.assertIsNotNone(result)

    def test_read_pdf(self):
        result = read_pdf('sample.pdf')
        self.assertIsNotNone(result)

    def test_read_csv(self):
        result = read_csv('sample.csv')
        self.assertIsNotNone(result)

    def test_read_json(self):
        result = read_json('sample.json')
        self.assertIsNotNone(result)

    def test_log_to_excel(self):
        # Dummy data for logging
        data = ["This is a test."]
        log_to_excel(data, "test_file")
        self.assertTrue(os.path.exists('doc_log.xlsx'))


class TestLoggingFunctions(unittest.TestCase):
    def test_log_document(self):
        # Assume 'sample.txt' is a test document in your project directory
        log_document('sample.txt')
        # Check if 'doc_log.xlsx' is created
        self.assertTrue(os.path.exists('doc_log.xlsx'))

    def test_log_excel(self):
        # Mock data for testing
        data = pd.DataFrame({'Document Name': ['sample.txt'],
                             'Content': ['Example content'],
                             'Timestamp': ['2024-10-10']})
        log_to_excel(data)
        # Check if data was logged
        logged_data = pd.read_excel('doc_log.xlsx')
        self.assertIn('sample.txt', logged_data['Document Name'].values)


if __name__ == '__main__':
    unittest.main()
