
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from .logger import logger
from .config import settings
from .pipeline.generate import run_full_pipeline

def job():
    logger.info("Scheduler tick: running pipeline")
    run_full_pipeline()

def main():
    sched = BlockingScheduler()
    minute, hour, dom, month, dow = settings.cron.split()
    sched.add_job(job, CronTrigger(minute=minute, hour=hour, day=dom, month=month, day_of_week=dow))
    logger.info("Starting scheduler with cron %s", settings.cron)
    sched.start()

if __name__ == "__main__":
    main()
