|pypi| |build status| |pyver|

HCLI hai
========

HCLI hai is a python package wrapper that contains an HCLI sample application (hai); hai is an HCLI for interacting with Anthropic's Claude models via terminal input and output streams.

----

HCLI hai wraps hai (an HCLI) and is intended to be used with an HCLI Client [1] as presented via an HCLI Connector [2].

You can find out more about HCLI on hcli.io [3]

[1] https://github.com/cometaj2/huckle

[2] https://github.com/cometaj2/hcli_core

[3] http://hcli.io

Installation
------------

HCLI hai requires a supported version of Python and pip.

You'll need an HCLI Connector to run hai. For example, you can use HCLI Core (https://github.com/cometaj2/hcli_core), a WSGI server such as Green Unicorn (https://gunicorn.org/), and an HCLI Client like Huckle (https://github.com/cometaj2/huckle).


.. code-block:: console

    pip install hcli-hai
    pip install hcli-core
    pip install huckle
    pip install gunicorn
    gunicorn --workers=1 --threads=1 -b 127.0.0.1:8000 "hcli_core:connector(\"`hcli_hai path`\")"

Usage
-----

Open a different shell window.

Setup the huckle env eval in your .bash_profile (or other bash configuration) to avoid having to execute eval everytime you want to invoke HCLIs by name (e.g. hai).

Note that no CLI is actually installed by Huckle. Huckle reads the HCLI semantics exposed by the API via HCLI Connector and ends up behaving *like* the CLI it targets.


.. code-block:: console

    huckle cli install http://127.0.0.1:8000
    eval $(huckle env)
    hai help

Versioning
----------

This project makes use of semantic versioning (http://semver.org) and may make use of the "devx",
"prealphax", "alphax" "betax", and "rcx" extensions where x is a number (e.g. 0.3.0-prealpha1)
on github.

Supports
--------

- Chatting via input/output streams (e.g. via pipes).
- .hai folder structure in a users's home directory to help track hai configuration and contexts.
- Creating, listing, deleting and changing conversation contexts.
- Automatic title creation based on context
- Custom context naming to help organize contexts
- Behavior setting to allow for persistent chat behavior (e.g. the Do Anything Now (DAN) prompt).
- Conversation vibing via detailed plans and HCLI integration to allow for external tool use.
  - This allows for capabilities enhancements (e.g. web search, git repo interaction, terminal use, etc.).
- hcli-problem-details use to help relay RFC 9457 problem details back to the HCLI client.

To Do
-----

- A memory layer for the the AI HCLI (hai).
    - Automatic context switching per NLP on received input stream.
    - Context blending to mary different contexts.
    - Automatic context compression to yield a more substantial memory footprint per context window.
- A shell mode for the AI HCLI (hai) to enable shell CLI execution per sought goal.
- Changing the vibing behavior should be made possible; it is currently locked in to HCLI integration and planning.
- Support multi-process and multi-context to allow for multiple parallel vibes or conversations without conflict.

Bugs
----

- An occasional thread exhaustion requires hcli_hai to be relaunched.

.. |build status| image:: https://circleci.com/gh/cometaj2/hcli_hai.svg?style=shield
   :target: https://circleci.com/gh/cometaj2/hcli_hai
.. |pypi| image:: https://img.shields.io/pypi/v/hcli-hai?label=hcli-hai
   :target: https://pypi.org/project/hcli-hai
.. |pyver| image:: https://img.shields.io/pypi/pyversions/hcli-hai.svg
   :target: https://pypi.org/project/hcli-hai
