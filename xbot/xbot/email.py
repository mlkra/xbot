# Copyright (C) 2022  Michał Krasoń
from email.message import EmailMessage
from smtplib import SMTP

from xbot.settings import settings


def send_message(message: EmailMessage):
    with SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.send_message(message, "xbot@localhost", "me@localhost")
