import imaplib
import smtplib as smtp
import ssl
from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiogram import Bot

from app.helpers.constants import (imapMailPort, imapMailServer, smtpMailServer, user_id,
                                   smtpMailPort, mailPassword, mailAddress, timeout)


def check_emails() -> list[str]:
    try:
        imap_client = imaplib.IMAP4_SSL(imapMailServer, port=imapMailPort, ssl_context=ssl.create_default_context())
        imap_client.login(mailAddress, mailPassword)
        imap_client.select("inbox")
        emails = []

        status, messages = imap_client.search(None, "UNSEEN")

        if status == "OK" and messages[0]:
            message_ids = messages[0].split()
            for message_id in message_ids:
                _, msg_data = imap_client.fetch(message_id, "(RFC822)")
                email_message = message_from_bytes(msg_data[0][1])
                text = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            text += part.get_payload()
                else:
                    text += email_message.get_payload()[0].get_payload(decode=False)

                notification_text = (f"From: {email_message['From']}\n" +
                                     f"Subject: {email_message['Subject']}\n" +
                                     f"Date: {email_message['Date']}\n" +
                                     f"Text:{text}\n")
                emails.append(notification_text)

        imap_client.logout()
        return emails
    except Exception as e:
        print(e)
        return []


def send_email(email) -> bool:
    try:
        with smtp.SMTP_SSL(smtpMailServer, smtpMailPort, timeout=timeout) as client:
            client.login(mailAddress, mailPassword)
            client.sendmail(mailAddress, [email['To']], email.as_string())
            client.close()
        return True
    except Exception as e:
        print(e)
        return False


def build_email(to, subject, body) -> MIMEMultipart:
    email_message = MIMEMultipart()
    email_message['From'] = mailAddress
    email_message['To'] = to
    email_message['Subject'] = subject
    email_message.attach(MIMEText(body, 'plain'))
    return email_message


async def check_emails_job(bot: Bot):
    emails = check_emails()
    if len(emails) == 0:
        return
    else:
        text = f'You have {len(emails)} new email(s)\n'
        for email in emails:
            text += email + '\n'
            pass
    await bot.send_message(user_id, text)
