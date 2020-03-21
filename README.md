MailMerge
================

Simple service which will import document attachments from SMTP account into a [Papermerge Project instance](https://github.com/ciur/papermerge) via REST API

## Usage

Create a configuration file e.g. mgmail.config.py
Run::
    
        mgmail --config /path/to/config.py

## Configuration file


Configuration file must have .py extention and be a valid python file, example::

    imap_server = "mail.paper.net"
    username = "<username>"
    password = "<pass>"
    api_key = "<API KEY>"
    papermerge_url = "<URL>"  # e.g. http://localhost:8000

## Configuration Settings
    
* ``imap_server`` is, well, your imap server.
* ``username`` and ``password`` - your imap user account
* ``api_key`` is papermerge's API key.
* Get your api_key as explained [here](https://papermerge.readthedocs.io/en/latest/rest_api.html#get-a-token)
* ``papermerge_url`` - paparmerge server instance url (with scheme i.e with http:// or https:// prefix)
