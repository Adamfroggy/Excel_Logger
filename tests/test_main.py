import unittest
from main import read_txt, read_docx, read_pdf, read_csv, read_json, \
                log_to_excel
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


if __name__ == '__main__':
    unittest.main()
