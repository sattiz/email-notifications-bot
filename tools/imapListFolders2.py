from imapclient import IMAPClient
from imapclient import imap_utf7
from dotenv import load_dotenv
import os

load_dotenv()

mailServer = os.environ['IMAP_MAIL_SERVER']
mailAddress = os.environ['IMAP_MAIL_USERNAME']
mailPassword = os.environ['IMAP_MAIL_PASSWORD']

with IMAPClient(mailServer, use_uid=True, ssl=True) as imap:
    imap.login(mailAddress, mailPassword)
    folders_containers = imap.list_folders()

    for folder_tuple in folders_containers:
        print (imap_utf7.decode(folder_tuple[2]))

    imap.logout()
