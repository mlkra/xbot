# Copyright (C) 2022  Michał Krasoń
from email.message import EmailMessage

from tests.mailhog_client import get_message, get_message_content, get_message_subject
from xbot.email import send_message


def test_sending_message():
    message = EmailMessage()
    message_subject = "Test message"
    message_content = "This is a test message."
    message["Subject"] = message_subject
    message.set_content(message_content)

    send_message(message)

    received_message = get_message()
    assert received_message["From"]["Mailbox"] == "xbot"
    assert received_message["From"]["Domain"] == "localhost"
    assert received_message["To"][0]["Mailbox"] == "me"
    assert received_message["To"][0]["Domain"] == "localhost"
    assert get_message_subject(received_message) == message_subject
    assert get_message_content(received_message) == message_content
