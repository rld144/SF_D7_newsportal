import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import date, timedelta
from django.contrib.auth.models import Group
from django.core.mail import mail_managers, send_mail
from newsportal.models import Post

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    reciptions = Group.objects.get(name='recipients')
    time = date.today() - timedelta(days=7)
    posts = Post.objects.filter(date__gt=time)
    msg = ''
    for post in posts:
        msg += f'{post.header}, http://127.0.0.1:8000/news/{post.pk}\n'
    send_mail(
        subject=f'Новости и статьи за последнию неделю начинася с {time}',
        # имя клиента и дата записи будут в теме для удобства
        message=msg,
        # сообщение с кратким описанием проблемы
        from_email='',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=reciptions.user_set.all().exclude(email='').values_list('email', flat=True)
        # здесь список получателей. Например, секретарь, сам врач и т. д.
    )
    print('hello from job')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day='*/7'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")