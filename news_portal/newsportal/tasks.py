from celery import shared_task
from django.core.mail import mail_managers, send_mail
from .models import Post
from django.contrib.auth.models import Group
from newsportal.models import Post
from datetime import date, timedelta


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@shared_task
def notify_news_celery(id):
    post = Post.objects.get(pk=id)
    reciptions = Group.objects.get(name='recipients')
    send_mail(
        subject=f'{post.header}',
        # имя клиента и дата записи будут в теме для удобства
        message=f'{post.preview()}, http://127.0.0.1:8000/news/{post.pk}',   # сообщение с кратким описанием проблемы
        from_email='',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=reciptions.user_set.all().exclude(email='').values_list('email', flat=True)  # здесь список получателей. Например, секретарь, сам врач и т. д.
    )


@shared_task
def scheduler_week():
    reciptions = Group.objects.get(name='recipients')
    time = date.today() - timedelta(days=7)
    posts = Post.objects.filter(date__gt=time)
    msg = ''
    for post in posts[::-1]:
        msg += f'{post.header}, http://127.0.0.1:8000/news/{post.pk}, {post.date}\n'
    send_mail(
        subject=f'Новости и статьи за последнию неделю начинася с {time}',
        # имя клиента и дата записи будут в теме для удобства
        message=msg,
        # сообщение с кратким описанием проблемы
        from_email='',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=reciptions.user_set.all().exclude(email='').values_list('email', flat=True)
        # здесь список получателей. Например, секретарь, сам врач и т. д.
    )
