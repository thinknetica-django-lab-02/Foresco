import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.contrib.auth.models import User
from main.models import Product
from main.mail_utils import send_mail_to_user

logger = logging.getLogger(__name__)


def new_products_notification():
    # New products list
    new_products = Product.objects.filter(noticed=False).values('product_name')
    if new_products:
        new_product_list = list()
        for new_product in new_products:
            new_product_list.append(new_product['product_name'])
        new_products_str = ', '.join(new_product_list)
        # Users with emails list
        mail_users = User.objects.filter(email__gt='').values('email', 'last_name', 'first_name')
        for mail_user in mail_users:
            send_mail_to_user(
                mail_user['email'],
                'Out shop got new products!',
                f"""Dear {mail_user['first_name']} {mail_user['last_name']},
                check our new products: {new_products_str}."""
            )
        # Set all products noticed
        Product.objects.filter(noticed=False).update(noticed=True)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            new_products_notification,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="new_products_notification",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'new_products_notification'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
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
