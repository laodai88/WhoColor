# -*- coding: utf-8 -*-
"""

:Authors:
    Felix Stadthaus,
    Kenan Erdogan
"""
import re

REGEX_HELPER_PATTERN = 'WIKICOLORLB'

SPECIAL_MARKUPS = (
    # Internal wiki links
    {
        'type': 'block',
        'start_regex': re.compile(r'\[\['),
        'end_regex': re.compile(r'\]\]'),
        'no_spans': False,
        'no_jump': False,
    },
    # External links
    {
        'type': 'block',
        'start_regex': re.compile(r'\['),
        'end_regex': re.compile(r'\]'),
        'no_spans': False,
        'no_jump': False,
    },
    # Template tags and similar
    {
        'type': 'block',
        'start_regex': re.compile(r'{{'),
        'end_regex': re.compile(r'}}'),
        'no_spans': True,  # no span is added around this element,
        'no_jump': False
    },
    # Reference tags - only start ref tag and attributes.
    # Closing ref is detected by 'General HTML tag' regex
    {
        'type': 'block',
        'start_regex': re.compile(r'<ref'),
        'end_regex': re.compile(r'>'),
        'no_spans': True,
        'no_jump': False
    },
    # Math, timeline, nowiki tags
    {
        'type': 'block',
        'start_regex': re.compile(r'<(math|timeline|nowiki)[^>]*>'),
        'end_regex': re.compile(r'</(math|timeline|nowiki)>'),
        'no_spans': True,
        'no_jump': False
    },
    # General HTML tag - only for text between < and > (tag name and attributes)
    {
        'type': 'block',
        'start_regex': re.compile(r'<'),
        'end_regex': re.compile(r'>'),
        'no_spans': True,
        'no_jump': False
    },
    # Headings
    {
        'type': 'single',
        'start_regex': re.compile(r'(=+|;)'),
        'end_regex': None,
        'no_spans': True,
        'no_jump': True
    },
    # Lists and blocks
    {
        'type': 'block',
        'start_regex': re.compile(r'[\\*#\\:]*;'),
        'end_regex': re.compile(r'\\:'),
        'no_spans': True,
        'no_jump': False
    },
    {
        'type': 'single',
        'start_regex': re.compile(r'[\\*#:]+'),
        'end_regex': None,
        'no_spans': True,
        'no_jump': True
    },
    # Horizontal lines
    {
        'type': 'single',
        'start_regex': re.compile(r'-----*'),
        'end_regex': None,
        'no_spans': True,
        'no_jump': True
    },
    # Table formatting
    # {
    #     'type': 'single',
    #     'start_regex': re.compile(r'(?<={})({\\||\\|}|\\|-|\\|\\+|\\|\\||)'.format(REGEX_HELPER_PATTERN)),
    #     'end_regex': None,
    #     'no_spans': True,
    #     'no_jump': True
    # },
    {
        'type': 'block',
        'start_regex': re.compile(r'{\|'),
        'end_regex': re.compile(r'\|}'),
        'no_spans': True,
        'no_jump': False
    },
    # Linebreaks
    {
        'type': 'single',
        'start_regex': re.compile(r'({})+'.format(REGEX_HELPER_PATTERN)),
        'end_regex': None,
        'no_spans': True,
        'no_jump': True
    },
    # HTML Escape Sequences
    {
        'type': 'single',
        'start_regex': re.compile(r'(&nbsp;|&euro;|&quot;|&amp;|&lt;|&gt;|&nbsp;|&(?:[a-z\d]+|#\d+|#x[a-f\d]+);)'),
        'end_regex': None,
        'no_spans': True,
        'no_jump': True
    },
    # Magic words
    {
        'type': 'single',
        'start_regex': re.compile(r'__(NOTOC|FORCETOC|TOC|NOEDITSECTION|NEWSECTIONLINK|NONEWSECTIONLINK|NOGALLERY|'
                                  r'HIDDENCAT|NOCONTENTCONVERT|NOCC|NOTITLECONVERT|NOTC|START|END|INDEX|NOINDEX|'
                                  r'STATICREDIRECT|DISAMBIG)__'),
        'end_regex': None,
        'no_spans': True,
        'no_jump': True
    },
    # Apostrophes for formatting
    {
        'type': 'single',
        'start_regex': re.compile(r'\'\'+'),
        'end_regex': None,
        'no_spans': True,
        'no_jump': True
    }
)
