import smtplib
from email.message import EmailMessage

from app.domain.common.models import User


async def send_hello(user: User):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение регистрации"
    msg['From'] = email_address
    msg['To'] = user.email
    msg.set_content(
        f"""\
        Вы успешно зарегистрировались на платформе Путеводитель по необычным местам!
        """
    )

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
