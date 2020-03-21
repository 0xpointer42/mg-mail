import logging
import ssl
import email
import tempfile
from imapclient import IMAPClient


logger = logging.getLogger(__name__)


def read_email_message(message):
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
                #Document.import_file(
                #    username=username,
                #    filepath=temp.name,
                #    file_title=part.get_filename(),
                #    delete_after_import=False,
                #    start_ocr_async=ocr_action,
                #    upload=upload_action
                #)
                imported_count += 1

    return imported_count


def import_attachment(
    imap_server,
    username,
    password,
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
            imported_count = read_email_message(email_message)

    return imported_count
