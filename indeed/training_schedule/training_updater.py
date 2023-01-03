from apscheduler.triggers.cron import CronTrigger

from .algs import Trainer
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_job
from django.conf import settings

from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution, logger
from django_apscheduler import util


def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def start():
    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # wind model training :
    scheduler.add_job(Trainer.wind_train,
                      trigger=CronTrigger(minute="*/30"),  # Every n minutes
                      id="Wind_model_training",  # The `id` assigned to each job MUST be unique
                      max_instances=1,  # number of jobs (with same job_id) allowed to run simultaneously
                      replace_existing=True,  # replace job that was not run
                      close_old_connection=True
                      )
    logger.info("Added job 'Wind_model_training'.")

    # solar model training :
    scheduler.add_job(Trainer.solar_train,
                      trigger=CronTrigger(minute="*/20"),
                      id="Solar_model_training",
                      max_instances=1,
                      replace_existing=True,
                      )

    logger.info("Added job 'Solar_model_training'.")

    # Delete old jobs in DB that have been executed
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
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
