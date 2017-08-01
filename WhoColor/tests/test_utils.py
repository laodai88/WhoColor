import unittest
from WhoColor.utils import *

class TestUtils(unittest.TestCase):
    def test_wikiwho_from_page_id(self):
        # Page ID of 'Selfie'
        WikiWhoRevContent(page_id=38956275).get_tokens()

    def test_wikiwho_from_page_title(self):
        WikiWhoRevContent(page_title='Selfie').get_tokens()

    def test_wikiwho_from_rev_id(self):
        # First revision of 'Selfie'
        WikiWhoRevContent(page_title='Selfie', rev_id=547645475).get_tokens()
