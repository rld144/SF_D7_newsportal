from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, send_mail
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .tasks import notify_news_celery, notify_news_category_celery


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_news(sender, instance, created, **kwargs):
    notify_news_celery.delay(instance.pk)
    notify_news_category_celery.delay(instance.pk)
    # reciptions = Group.objects.get(name='recipients')
    # send_mail(
    #     subject=f'{instance.header}',
    #     # имя клиента и дата записи будут в теме для удобства
    #     message=f'{instance.preview()}, http://127.0.0.1:8000/news/{instance.pk}',   # сообщение с кратким описанием проблемы
    #     from_email='ayaal.everstov@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
    #     recipient_list=reciptions.user_set.all().exclude(email='').values_list('email', flat=True)  # здесь список получателей. Например, секретарь, сам врач и т. д.
    # )
