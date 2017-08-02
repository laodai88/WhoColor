import unittest
from WhoColor.utils import WikiWhoRevContent


class TestUtils(unittest.TestCase):
    def test_wikiwho_from_page_id(self):
        # Page ID of 'Selfie'
        page_id = 38956275
        ww_rev_content = WikiWhoRevContent(page_id=page_id)
        # test if request data is correct
        request_data = ww_rev_content._prepare_request()
        data = {'url': 'https://api.wikiwho.net/api/v1.0.0-beta/rev_content/page_id/{}/'.format(page_id),
                'params': {'o_rev_id': 'true', 'editor': 'true', 'token_id': 'false', 'out': 'true', 'in': 'true'}}
        assert request_data == data
        # check if no errors
        ww_rev_content.get_revisions_and_tokens()

    def test_wikiwho_from_page_title(self):
        page_title = 'Selfie'
        ww_rev_content = WikiWhoRevContent(page_title=page_title)
        # test if request data is correct
        request_data = ww_rev_content._prepare_request()
        data = {'url': 'https://api.wikiwho.net/api/v1.0.0-beta/rev_content/{}/'.format(page_title),
                'params': {'o_rev_id': 'true', 'editor': 'true', 'token_id': 'false', 'out': 'true', 'in': 'true'}}
        assert request_data == data
        # check if no errors
        ww_rev_content.get_revisions_and_tokens()

    def test_wikiwho_from_rev_id(self):
        # First revision of 'Selfie'
        page_title = 'Selfie'
        rev_id = 547645475
        ww_rev_content = WikiWhoRevContent(page_title=page_title, rev_id=rev_id)
        # test if request data is correct
        request_data = ww_rev_content._prepare_request()
        data = {'url': 'https://api.wikiwho.net/api/v1.0.0-beta/rev_content/{}/{}/'.format(page_title, rev_id),
                'params': {'o_rev_id': 'true', 'editor': 'true', 'token_id': 'false', 'out': 'true', 'in': 'true'}}
        assert request_data == data
        # check if no errors
        ww_rev_content.get_revisions_and_tokens()
