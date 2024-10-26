from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from config.settings import (
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
)

conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL_HOST_USER,
    MAIL_PASSWORD=EMAIL_HOST_PASSWORD,
    MAIL_FROM=EMAIL_HOST_USER,
    MAIL_PORT=EMAIL_PORT,
    MAIL_SERVER=EMAIL_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


async def send_email(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)

    await fm.send_message(message)
