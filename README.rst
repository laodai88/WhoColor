
.. image:: https://github.com/wikiwho/WhoColor/blob/dev/WhoColor/static/whocolor/readme/whocolorpreview.png

WhoColor
========
The WhoColor userscript colors Wikipedia articles based on by-word authorship.

Take a look at http://f-squared.org/whovisual/ for more information.

Requirements and Installation
=============================

`requests <http://docs.python-requests.org/en/master/>`_ package is required to get revision meta data and text from Wikipedia api.


Install WhoColor package (server code) using ``pip``::

    pip install WhoColor


Install WhoColor user script using ``Tampermonkey`` or ``Greasemonkey`` for Chrome and Firefox:

- First install one of:
 - `Tampermonkey <https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo/>`_ for Chrome
 - `Tampermonkey <https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/>`_ for Firefox
 - `Greasemonkey <https://addons.mozilla.org/en-US/firefox/addon/greasemonkey/>`_ for Firefox
- Open `user script <https://github.com/wikiwho/WhoColor/blob/dev/userscript/whocolor.user.js>`_ and click on ``Raw`` button on the top right
- ``Tampermonkey`` or ``Greasemonkey`` will automatically detect the user script and ask to install it
- Open an article in Wikipedia and now you should see the ``WhoColor`` to the left of the default "Read" tab in the head navigation of the article

Contact
=======
* Fabian Floeck: fabian.floeck[.]gesis.org
* Kenan Erdogan: kenan.erdogan[.]gesis.org

License
=======
This work is licensed under MIT (some assets have other licenses, more detailed information in the LICENSE file).


**Developed at Karlsruhe Institute of Technology and GESIS - Leibniz Institute for the Social Sciences**
