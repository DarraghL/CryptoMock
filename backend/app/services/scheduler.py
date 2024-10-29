from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False

    def init_app(self, app, price_updater):
        """Initialize scheduler with Flask app"""
        self.app = app
        
        # Add price update job - every 5 minutes
        self.scheduler.add_job(
            func=price_updater.update_prices,
            trigger=IntervalTrigger(minutes=5),
            id='Update cryptocurrency prices',
            name='Update cryptocurrency prices',
            replace_existing=True
        )
        
        # Add cleanup job - daily at midnight
        self.scheduler.add_job(
            func=price_updater.cleanup_old_prices,
            trigger=IntervalTrigger(days=1),
            id='Cleanup old price history',
            name='Cleanup old price history',
            replace_existing=True
        )
        
        # Start scheduler
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started successfully")

    def shutdown(self):
        """Shutdown the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler shutdown successfully")