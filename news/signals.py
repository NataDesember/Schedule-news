from smtplib import SMTPDataError

from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, mail_admins
from .models import Post


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    if created:
        subject = f'New post: {instance.title} at {instance.time_in.strftime("%d %m %Y")}'
        try:
            mail_admins(
                subject=subject,
                message=instance.text,
            )
        except SMTPDataError:
            pass