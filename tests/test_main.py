import unittest
import pandas as pd
from main import read_txt, read_docx, read_pdf, read_csv, read_json, \
                log_to_excel, parse_document
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


class TestFileNotFound(unittest.TestCase):
    def test_read_txt_file_not_found(self):
        result = read_txt('non_existent.txt')
        self.assertIsNone(result)

    def test_read_docx_file_not_found(self):
        result = read_docx('non_existent.docx')
        self.assertIsNone(result)

    def test_read_pdf_file_not_found(self):
        result = read_pdf('non_existent.pdf')
        self.assertIsNone(result)

    def test_read_csv_file_not_found(self):
        result = read_csv('non_existent.csv')
        self.assertIsNone(result)

    def test_read_json_file_not_found(self):
        result = read_json('non_existent.json')
        self.assertIsNone(result)


class TestUnsupportedFile(unittest.TestCase):
    def test_parse_document_unsupported_format(self):
        result = parse_document('sample.unsupported')
        self.assertIsNone(result)


class TestEmptyData(unittest.TestCase):
    def test_read_empty_txt(self):
        result = read_txt('empty.txt')
        self.assertEqual(result, [])

    def test_read_empty_csv(self):
        result = read_csv('empty.csv')
        self.assertEqual(result, [])


class TestBatchLogging(unittest.TestCase):
    def test_batch_log_to_excel(self):
        data1 = ["Test content for file 1."]
        data2 = ["Test content for file 2."]
        log_to_excel(data1, 'file1.txt')
        log_to_excel(data2, 'file2.txt')

        # Check that both files are logged
        logged_data = pd.read_excel('doc_log.xlsx')
        self.assertIn('file1.txt', logged_data['Document Name'].values)
        self.assertIn('file2.txt', logged_data['Document Name'].values)


class TestDataIntegrity(unittest.TestCase):
    def test_data_integrity_after_log(self):
        data = ["Test content."]
        file_name = "test_integrity.txt"
        log_to_excel(data, file_name)

        logged_data = pd.read_excel('doc_log.xlsx')

        # Ensure the logged data matches
        logged_content = logged_data[logged_data['Document Name'] == file_name]
        ['Content'].values[0]
        self.assertEqual(logged_content.strip(), "Test content.")

        logged_timestamp = logged_data[logged_data
                                       ['Document Name'] == file_name]
        ['Timestamp'].values[0]
        self.assertIsNotNone(logged_timestamp)  # Ensure timestamp exists


if __name__ == '__main__':
    unittest.main()
