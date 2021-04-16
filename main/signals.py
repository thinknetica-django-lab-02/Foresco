from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail


def send_mail_to_user(user_email):
    send_mail(
        'You are registered in DjangoLab',
        'Welcome to our project!',
        'mailrobot@clever-soft.ru',
        [user_email, ],
        fail_silently=False,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='common users'))
        instance.save()
