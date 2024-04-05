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


class EmailService:
    def __init__(self, email_address, email_password):
        self.email_address = email_address
        self.email_password = email_password

    async def send_password_reset_email(self, user: User, code: str):
        msg = EmailMessage()
        msg['Subject'] = "Сброс пароля"
        msg['From'] = self.email_address
        msg['To'] = user.email
        msg.set_content(
            f"""\
            Здравствуйте,

            Вы запросили сброс пароля на платформе Путеводитель по необычным местам.

            Код для сброса пароля: {code}

            Если вы не запрашивали сброс пароля, проигнорируйте это письмо.

            С уважением,
            Ваша команда Путеводитель по необычным местам
            """
        )

        with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(msg)
