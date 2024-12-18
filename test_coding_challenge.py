import unittest
import coding_challenge
import pathlib
import os

class TestCaseBase(unittest.TestCase):

    # Test to check that the file is created for the correct name
    def test_file_created(self):
        path = pathlib.Path("output/amazon.txt")
        print(path)
        
        coding_challenge.main(['https://www.amazon.co.uk/'])
        if not pathlib.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))
        
    # Test to check that the code still passes if a non-link is passed
    def test_faulty_link(self):
        # 2 real links passed and 1 faulty one. Would expect 2 files to be created
        coding_challenge.main(['test_faulty_link', 'https://www.amazon.co.uk/', 'https://www.youtube.com/'])
        expected_output = ['amazon.txt', 'youtube.txt']
        self.assertEqual(os.listdir('output/'), expected_output)

    # Test to check that the queue is being populated
    def test_queue_population(self):
        coding_challenge.producer(['https://www.amazon.co.uk/', 'https://www.youtube.com/'])
        q_size = coding_challenge.queue.qsize()
        # q_size should equal the amount of valid URLs passed plus 1 for the sentinel value: hence 3
        self.assertEqual(q_size, 3)

    def test_clean_urls(self):
        # Test for duplicate URLs and invalid URLs
        urls = [
            "https://example.com",
            "https://example.com",
            "http://example.com",
            "invalid_url",
            "ftp://example.com"
        ]
        expected_output = ['https://example.com', 'http://example.com']
        self.assertEqual(coding_challenge.clean_urls(urls), expected_output)

if __name__ =='__main__':
    unittest.main()