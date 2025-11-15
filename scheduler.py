"""
Scheduled tasks module
"""
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from database import Database
from wechat_bot import WeChatBot
from message_formatter import format_daily_report


def daily_report_job():
    """
    Daily report job that runs at 12:01 AM
    Reports previous day's statistics
    """
    print(f"Running daily report job at {datetime.now()}")
    
    try:
        # Get yesterday's date
        yesterday = datetime.now().date() - timedelta(days=1)
        
        # Get statistics
        db = Database()
        stats = db.get_combined_stats(yesterday, yesterday)
        
        # Format and send message
        message = format_daily_report(stats)
        bot = WeChatBot()
        bot.send_text_message(message)
        
        print("Daily report sent successfully")
    except Exception as e:
        print(f"Error in daily report job: {str(e)}")


def start_scheduler():
    """
    Start the background scheduler for periodic tasks
    
    Returns:
        BackgroundScheduler: The scheduler instance
    """
    scheduler = BackgroundScheduler()
    
    # Schedule daily report at 12:01 AM
    scheduler.add_job(
        daily_report_job,
        'cron',
        hour=0,
        minute=5,
        id='daily_report',
        name='Daily Report Job',
        replace_existing=True
    )
    
    scheduler.start()
    print("Scheduler started. Daily report scheduled for 12:01 AM")
    
    return scheduler
