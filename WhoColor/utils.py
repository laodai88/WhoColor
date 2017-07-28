# -*- coding: utf-8 -*-
"""

:Authors:
    Kenan Erdogan
"""
import requests
import hashlib


class WikipediaRevText(object):
    """
    Example usage:
        wp_rev_text_obj = WikipediaRevText(page_title='Cologne', page_id=6187)
        # to get rev wiki text from wp api
        rev_data = wp_rev_text_obj.get_rev_wiki_text()
        # to convert (extended) wiki text into html by using wp api
        rev_extended_html = wp_rev_text_obj.convert_wiki_text_to_html(wiki_text=rev_data['rev_text'])
    """

    def __init__(self, page_title=None, page_id=None, rev_id=None):
        """
        :param page_title: Title of an article.
        :param page_id: ID of an article
        :param rev_id: Revision id to get wiki text.
        """
        self.page_id = page_id
        self.page_title = page_title
        self.rev_id = rev_id

    def _prepare_request(self, wiki_text=None):
        data = {'url': 'https://en.wikipedia.org/w/api.php'}
        if wiki_text is None:
            params = {'action': 'query', 'prop': 'revisions',
                      'rvprop': 'content|ids', 'rvlimit': '1', 'format': 'json'}
            if self.page_id:
                params.update({'pageids': self.page_id})
            elif self.page_title:
                params.update({'titles': self.page_title})
            if self.rev_id is not None:
                params.update({'rvstartid': self.rev_id})  # , 'rvendid': rev_id})
        else:
            params = {'action': 'parse', 'title': self.page_title,
                      'format': 'json', 'text': wiki_text, 'prop': 'text'}
        data['data'] = params
        return data

    def _make_request(self, data):
        response = requests.post(**data).json()
        return response

    def get_rev_wiki_text(self):
        """
        If no rev id is given, text of latest revision is returned.
        If both article id and title are given, id is used in query.
        """
        if self.page_id is None and self.page_title is None:
            raise Exception('Please provide id or title of the article.')

        data = self._prepare_request()
        response = self._make_request(data)

        if 'error' in response:
            return response
        pages = response['query']['pages']
        if '-1' in pages:
            return pages
        for page_id, page in response['query']['pages'].items():
            namespace = page['ns']
            revisions = page.get('revisions')
            if revisions is None:
                return None
            else:
                return {
                    'page_id': int(page_id),
                    'namespace': namespace,
                    'rev_id': revisions[0]['revid'],
                    'rev_text': revisions[0]['*']
                }

    def convert_wiki_text_to_html(self, wiki_text):
        """
        Title of the article is required.
        """
        if self.page_title is None:
            raise Exception('Please provide title of the article.')

        data = self._prepare_request(wiki_text)
        response = self._make_request(data)

        if 'error' in response:
            return response

        return response['parse']['text']['*']


class WikipediaUser(object):
    """
    Example usage to get names of given editor ids:
        editor_ids = set(('30764272', '1465', '5959'))
        wp_user_obj = WikipediaUser(editor_ids)
        editors = wp_user_obj.get_editor_names()
    """
    def __init__(self, editor_ids):
        # self.editor_ids = set(map(str, editor_ids))  # set of ids
        self.editor_ids = editor_ids  # set of ids

    def _prepare_request(self):
        params = {'action': 'query', 'list': 'users',
                  'format': 'json', 'ususerids': '|'.join(self.editor_ids)}
        return {
            'url': 'https://en.wikipedia.org/w/api.php',
            'data': params
        }

    def _make_request(self, data):
        response = requests.post(**data).json()
        return response

    def get_editor_names(self):
        editor_names = {}  # {editor_id: editor_name, ..}
        while True:
            data = self._prepare_request()
            response = self._make_request(data)

            if 'error' in response:
                return response
            users = response['query']['users']
            if '-1' in users:
                return users

            for user in users:
                editor_names[str(user['userid'])] = user.get('name', None)
                self.editor_ids.remove(str(user['userid']))
            if not self.editor_ids:
                self.editor_ids = set(editor_names.keys())
                return editor_names


class WikiWhoRevContent(object):
    """
    Example usage:
        ww_rev_content = WikiWhoRevContent(page_id=6187)
        wikiwho_tokens = ww_rev_content.get_tokens()
    """
    def __init__(self, page_id=None, page_title=None, rev_id=None):
        self.page_id = page_id
        self.page_title = page_title
        self.rev_id = rev_id

    def _prepare_request(self):
        if self.page_id:
            url_params = 'page_id/{}'.format(self.page_id)
        elif self.page_title:
            url_params = 'article_title/{}'.format(self.page_title)
        elif self.rev_id:
            url_params = 'article_title/{}/{}'.format(self.page_title, self.rev_id)
        ww_api_url = 'https://api.wikiwho.net/api/v1.0.0-beta'
        return {'url': '{}/rev_content/{}/'.format(ww_api_url, url_params),
                'params': {'o_rev_id': 'false', 'editor': 'true', 'token_id': 'false', 'out': 'true', 'in': 'true'}}

    def _make_request(self, data):
        response = requests.get(**data).json()
        return response

    def get_tokens(self):
        """
        Returns tokens of given article.
        If no rev id is given, tokens of latest revision is returned.
        """
        if self.page_id is None and self.page_title is None and self.rev_id is None:
            raise Exception('Please provide page id or page title or rev id.')
        data = self._prepare_request()
        response = self._make_request(data)
        _, rev_data = response['revisions'][0].popitem()

        # get editor names from wp api
        editor_ids = {t['editor'] for t in rev_data['tokens'] if not t['editor'].startswith('0|')}
        wp_users_obj = WikipediaUser(editor_ids)
        editor_names_dict = wp_users_obj.get_editor_names()

        # set editor and class names for each token
        # if registered user, class name is editor id
        for token in rev_data['tokens']:
            token['editor_name'] = editor_names_dict.get(token['editor'], token['editor'])
            if token['editor'].startswith('0|'):
                token['class_name'] = hashlib.md5(token['editor'].encode('utf-8')).hexdigest()
            else:
                token['class_name'] = token['editor']
            # TODO better conflict scores. remove also self reverts
            token['conflict_score'] = len(token['in']) + len(token['out'])
        return rev_data['tokens']
