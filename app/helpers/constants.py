import os

from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

# commands
START = 'start'
DATA = 'data'
SEND_MAIL = 'send_mail'
CANCEL = 'cancel'

# environmental variables
load_dotenv()
token = os.environ['TELEGRAM_BOT_TOKEN']
user_id = int(os.environ['TELEGRAM_USER_ID'])
imapMailServer = os.environ['IMAP_MAIL_SERVER']
imapMailPort = int(os.environ['IMAP_MAIL_PORT'])
smtpMailServer = os.environ['SMTP_MAIL_SERVER']
smtpMailPort = int(os.environ['SMTP_MAIL_PORT'])
mailAddress = os.environ['MAIL_USERNAME']
mailPassword = os.environ['MAIL_PASSWORD']
timeout = int(os.environ['TIMEOUT'])


# FSMs
class GetField(StatesGroup):
    waiting_for_email_addr = State()
    waiting_for_email_subj = State()
    waiting_for_email_text = State()
