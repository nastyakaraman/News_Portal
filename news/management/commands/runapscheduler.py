import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string


from news.models import Post, Subscription

logger = logging.getLogger(__name__)

def my_job():
    today = datetime.datetime.now()
    lastweek = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=lastweek)
    categories = set(posts.values_list('category__id', flat = True))
    subscribers = set(Subscription.objects.filter(category__in=categories).values_list('user__email', flat = True))

    html_content= render_to_string(
        'weekly_news.html',
        {
             'posts': posts,
        }
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(
            subject='Еженедельная рассылка',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="16", minute="59"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")