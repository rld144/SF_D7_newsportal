from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, send_mail
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .tasks import notify_news_celery


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_news(sender, instance, created, **kwargs):
    notify_news_celery.delay(instance.pk)
