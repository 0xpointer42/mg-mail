MailMerge
================

Simple service which will import document attachments from SMTP account into a [Papermerge Project instance](https://github.com/ciur/papermerge) via REST API

Example of configuration file (mgmail.config.py)::

    imap_server = "mail.paper.net"
    username = "<username>"
    password = "<pass>"
    api_key = "<API KEY>"
    papermerge_url = "<URL>"  # e.g. http://localhost:8000

Configuration file must have .py extention and be a valid python script.
