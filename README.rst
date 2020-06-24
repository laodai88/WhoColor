
Current notes
===========
NOTE 1: This is a side project by `Faflo <https://github.com/faflo>`_ . I currently do not have the resources  to follow up on all issues with WhoColor. So **please feel free to submit pull requests** or tell someone you know that is knowledgable to submit them. I will comment on issues, and help with resolving them.  Pull requests can be done on the userscript, which will then be included by all clients. You can also help make the underyling API-code better, which lives in the /WhoColor/ folder. This, we will carefully review and then deploy to the underlying API, which we also run. 

NOTE 2: There is an official Firefox extension by the WMF created in collaboration with us that is much more refined than the userscript regarding the UI and some other things - although only offering provenance/authorship view, not conflict/age/history. Depending on what you need, this might be more suited for you: https://addons.mozilla.org/en-US/firefox/addon/whowrotethat/





WhoColor
========
The WhoColor userscript colors Wikipedia articles based on by-word authorship, gives color-coded information on conflicts and age and provides per-word revision histories.

Take a look at http://f-squared.org/whovisual/ for more information.

.. image:: https://github.com/wikiwho/WhoColor/blob/dev/WhoColor/static/whocolor/readme/whocolorpreview.png

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

Known Issues
=======
* Only works guaranteed with the default Mediawiki skin
* Check out the other issues https://github.com/wikiwho/WhoColor/issues


Contact
=======
* Fabian Floeck: f.floeck+wikiwho[.]gmail.com

License
=======
This work is licensed under MIT (some assets have other licenses, more detailed information in the LICENSE file).


**Developed at Karlsruhe Institute of Technology and GESIS - Leibniz Institute for the Social Sciences**
