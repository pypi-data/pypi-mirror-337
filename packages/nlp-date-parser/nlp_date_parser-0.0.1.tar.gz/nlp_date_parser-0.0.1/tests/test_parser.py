import unittest
from nlp_date_parser import NLPDateParser

class TestNLPDateParser(unittest.TestCase):
    def test_parse(self):
        parser = NLPDateParser()
        result = parser.parse("next Friday")
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
