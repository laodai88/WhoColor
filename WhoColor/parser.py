# -*- coding: utf-8 -*-
"""

:Authors:
    Felix Stadthaus,
    Kenan Erdogan
"""
from .special_markups import SPECIAL_MARKUPS, REGEX_HELPER_PATTERN


class WikiMarkupParser(object):
    """
    Explain how parser works: annotation etc...
    """
    def __init__(self, wiki_text, tokens):  # , revisions):
        # Saves the full wikipedia markup and all WikiWho tokens
        self.wiki_text = wiki_text
        self.wiki_text_low = ''  # to find tokens - wikiwho tokens are always in lower case
        self.tokens = tokens
        self.tokens_len = len(tokens)
        # self.revisions = revisions
        self.token = None

        # Saves the current positions
        self._token_index = 0
        self._wiki_text_pos = 0

        # Saves whether there is currently an open span tag
        self._open_span = False
        # Array that holds the starting positions of blocks (special elements) we already jumped into
        self._jumped_elems = set()

        # The return values of the parser (error can be an error description)
        self.extended_wiki_text = ''
        self.error = False
        self.present_editors = dict()  # {editor_id: [class_name, count], }

    def __set_token(self):
        self.token = None
        if self._token_index < self.tokens_len:
            self.token = self.tokens[self._token_index]
            if not self.token.get('end'):
                # if token is not already fetched.
                self.token['end'] = self._wiki_text_pos + \
                                    self.wiki_text_low[self._wiki_text_pos:].index(self.token['str']) + \
                                    len(self.token['str'])

                # string_pos = self.wiki_text_low[self._wiki_text_pos:].find(token['str'])
                # # if string_pos == -1:
                # #     self.error = 'Token ({}) not found in markup'.format(token['str'])
                # #     return None  # TODO: Handle this error correctly - actually this shouldn't be possible
                # token['end'] = self._wiki_text_pos + string_pos + len(token['str'])
                if self.token['editor'] in self.present_editors:
                    self.present_editors[self.token['editor']][2] += 1
                else:
                    self.present_editors[self.token['editor']] = [self.token['editor_name'],
                                                                  self.token['class_name'],
                                                                  1]

    def __get_first_regex(self, regex):
        first_match = None
        for match in regex.finditer(self.wiki_text):
            # search every time from the beginning of text
            if (first_match is None or first_match.start() > match.start()) and match.start() >= self._wiki_text_pos:
                # if match is first and starts after wiki text pos
                first_match = match
        if first_match is not None:
            return {'str': first_match.group(), 'start': first_match.start()}
        return None
        # NOTE this doesnt work because some regex contains positive look behind!
        # match = regex.search(self.wiki_text[self._wiki_text_pos:])
        # if match:
        #     return {
        #         'str': match.group(),
        #         'start': self._wiki_text_pos + match.start()
        #     }
        # return None

    def __get_special_elem_end(self, special_elem):
        # Get end position of current special markup element
        end_pos_data = {}
        if special_elem.get('end_len') is not None and special_elem.get('end') is not None:
            # if special markup is single (has no end regex)
            end_pos_data['start'] = special_elem['end']
            end_pos_data['len'] = special_elem['end_len']
            end_pos_data['end'] = end_pos_data['start'] + end_pos_data['len']
        else:
            end_regex = self.__get_first_regex(special_elem['end_regex'])
            if end_regex is not None:
                end_pos_data['start'] = end_regex['start']
                end_pos_data['len'] = len(end_regex['str'])
                end_pos_data['end'] = end_pos_data['start'] + end_pos_data['len']
        return end_pos_data

    def __get_next_special_element(self):
        # Get starting position of next special markup element
        next_ = {}
        for special_markup in SPECIAL_MARKUPS:
            found_markup = self.__get_first_regex(special_markup['start_regex'])
            if found_markup is not None and \
               (not next_ or next_['start'] > found_markup['start']) and \
               found_markup['start'] not in self._jumped_elems:
                next_ = special_markup
                next_['start'] = found_markup['start']
                next_['start_len'] = len(found_markup['str'])
                if next_['type'] == 'single':
                    # to be used in __get_special_elem_end - because it has no end regex
                    next_['end'] = next_['start']
                    next_['end_len'] = next_['start_len']
        return next_

    def __add_spans(self, token, close_only=False, open_only=False):
        """
        Explanation with possible inputs:
            If there is only an opened span:
                1) if open_only is True and close_only is False, close previous span and start new span (no_spans=False)
                2) if open_only is False and close_only is True, close previous span (no_spans=True)
                3) if open_only is False and close_only is False, close previous span and start new span (normal Token)
            If there is not an opened span:
                1) if close_only is False, start a new span (no_spans=False or normal Token)
                2) if close_only is True, do nothing (no_spans=True)

        If no_spans is False, then editor of first token of this special markup is added to whole special markup.
        """
        # editor_class = 'token-authorid-{}'.format(token['editor'])
        editor_class = 'token-authorid-{}'.format(token['class_name'])
        if self._open_span is True:
            # TODO: this check is commented, not sure if it was a good idea.
            # if open_only is True:
            #     return
            self.extended_wiki_text += '</span>'
            self._open_span = False
        if close_only is False:
            self.extended_wiki_text += '<span class="author-token {} author-tokenid-{}">'.\
                                       format(editor_class, self._token_index)
            self._open_span = True

    def __parse_wiki_text(self, add_spans=True, special_elem=None, no_jump=False):
        """

        :param add_spans: Flag to decide adding spans around tokens.
        :param special_elem: Current special element that parser is in.
        :param no_jump: Flag to prevent jumping into parsing special elements.
        :return: True if parsing is successful.
        """
        # Current WikiWho token
        self.__set_token()
        # Get end position of current special markup
        special_elem_end = self.__get_special_elem_end(special_elem) if special_elem else False
        # Get starting position of next special markup element in wiki text
        next_special_elem = self.__get_next_special_element()

        while self._wiki_text_pos < (len(self.wiki_text) - 1):
            if self.token is None:
                # No token left to parse
                # Add everything that's left to the end of the extended wiki text
                self.extended_wiki_text += self.wiki_text[self._wiki_text_pos: len(self.wiki_text)]
                self._wiki_text_pos = len(self.wiki_text)  # - 1
                return True

            # Don't jump anywhere if no_jump is set or if already in a special markup element
            if no_jump is False and (not special_elem_end or self._wiki_text_pos < special_elem_end['start']):
                if next_special_elem and \
                   (not special_elem_end or next_special_elem['start'] < special_elem_end['start']) and \
                   next_special_elem['start'] < self.token['end']:
                    # Special markup element was found before or reaching into token
                    # Or token itself is a start of special markup
                    self._jumped_elems.add(next_special_elem['start'])

                    if add_spans:
                        self.__add_spans(self.token,
                                         close_only=next_special_elem['no_spans'],
                                         open_only=not next_special_elem['no_spans'])

                    # NOTE: add_spans=False
                    # => no span will added into this special markup
                    # if no_spans=False, this special markup will have one span with editor of first token
                    self.__parse_wiki_text(add_spans=False,
                                           special_elem=next_special_elem,
                                           no_jump=next_special_elem['no_jump'])
                    # Current WikiWho token
                    # token = self.__get_token()
                    # Get position of end regex of current special markup
                    if special_elem:
                        special_elem_end = self.__get_special_elem_end(special_elem)
                    # Get starting position of next special markup element
                    next_special_elem = self.__get_next_special_element()
                    # if add_spans is True and next_special_elem['no_spans'] is True:
                    #     self.__add_spans(token)
                    continue

            # Is it end of special element?
            if special_elem_end and special_elem_end['end'] < self.token['end']:
                # Special element has been matched before the token
                # => Set position to special element's end
                self.extended_wiki_text += self.wiki_text[self._wiki_text_pos:special_elem_end['end']]
                self._wiki_text_pos = special_elem_end['end']
                return True

            # Add sequence author tags around token
            if add_spans:
                self.__add_spans(self.token)  # close and open span tag

            # add remaining token (and possible preceding chars) to resulting altered markup
            self.extended_wiki_text += self.wiki_text[self._wiki_text_pos:self.token['end']]
            self._wiki_text_pos = self.token['end']

            # Increase token index
            self._token_index += 1
            # Get new token
            self.__set_token()

        # Close opened tags
        if self._open_span:
            self.extended_wiki_text += "</span>"
            self._open_span = False
        return True

    def __set_present_editors(self):
        """
        Sort editors who owns tokens in given revision according to percentage of owned tokens in decreasing order.
        """
        self.present_editors = tuple(
            (editor_name, class_name, count*100.0/self.tokens_len)
            for editor_id, (editor_name, class_name, count) in
            sorted(self.present_editors.items(), key=lambda x: x[1][2], reverse=True)
        )

        # # TODO calculate editor scores directly from token data?
        # editors = defaultdict(int)
        # for t in self.tokens:
        #     editors[t['editor']] += 1
        # editor_ids = {e for e in editors if not e.startswith('0|')}
        # wp_users_obj = WikipediaUser(editor_ids)
        # editor_names_dict = wp_users_obj.get_editor_names()
        # self.present_editors = tuple((e, editor_names_dict.get(e, e), c*100.0/self.tokens_len)
        #                              for e, c in sorted(editors.items(), key=lambda x: x[1], reverse=True))

    def generate_extended_wiki_markup(self):
        """

        """
        # Add regex helper pattern into wiki text in order to easy regex search
        self.wiki_text = self.wiki_text.replace('\r\n', REGEX_HELPER_PATTERN).\
                                        replace('\n', REGEX_HELPER_PATTERN).\
                                        replace('\r', REGEX_HELPER_PATTERN)
        self.wiki_text_low = self.wiki_text.lower()

        self.__parse_wiki_text()
        self.__set_present_editors()

        # Remove regex patterns
        self.wiki_text = self.wiki_text.replace(REGEX_HELPER_PATTERN, '\n')
        self.extended_wiki_text = self.extended_wiki_text.replace(REGEX_HELPER_PATTERN, '\n')