import sys
import logging
import ssl
import email
import tempfile
import requests
from imapclient import IMAPClient


logger = logging.getLogger(__name__)


def upload_document(
    filepath,
    file_title,
    papermerge_url,
    api_key
):
    url = f"{papermerge_url}/api/document/upload/file1.pdf"
    headers = {
        'Authorization': f"Token {api_key}",
        "Content-Type": "application/binary",
    }
    data = open(filepath, 'rb').read()
    try:
        response = requests.put(
            url,
            headers=headers,
            data=data
        )
        if response.status_code == 401:
            print(f"Upload failed: {response.reason}")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to {papermerge_url}")
        sys.exit(1)


def read_email_message(message, papermerge_url, api_key):
    """
    message is an instance of python's module email.message
    """
    imported_count = 0

    for part in message.walk():
        # search for payload
        maintype = part.get_content_maintype()
        subtype = part.get_content_subtype()
        if maintype == 'application' and subtype == 'pdf':

            with tempfile.NamedTemporaryFile() as temp:
                temp.write(part.get_payload(decode=True))
                temp.flush()
                #    filepath=temp.name,
                #    file_title=part.get_filename(),
                # Upload document via api_key
                # something like curl -X POST -d "@file"  <server>/api/document/upload/file1 'Authentication: Token <token>'
                upload_document(
                    filepath=temp.name,
                    file_title=part.get_filename,
                    papermerge_url=papermerge_url,
                    api_key=api_key
                )
                imported_count += 1

    return imported_count


def import_attachment(
    imap_server,
    username,
    password,
    papermerge_url,
    api_key
):

    imported_count = 0

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    with IMAPClient(
        imap_server,
        ssl_context=ssl_context
    ) as server:
        server.login(username, password)
        server.select_folder('INBOX')
        messages = server.search(['UNSEEN'])

        logger.debug(
            f"IMAP UNSEEN messages {len(messages)}"
            f" for {username}"
        )

        for uid, message_data in server.fetch(
            messages, 'RFC822'
        ).items():
            email_message = email.message_from_bytes(
                message_data[b'RFC822']
            )
            imported_count = read_email_message(
                email_message,
                papermerge_url,
                api_key
            )

    return imported_count
