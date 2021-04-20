from django.core.mail import send_mail


def send_mail_to_user(user_email, title, message):
    send_mail(
        title,
        message,
        'mailrobot@clever-soft.ru',
        [user_email, ],
        fail_silently=False,
    )
