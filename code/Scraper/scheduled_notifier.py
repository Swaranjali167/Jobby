import schedule
import time
import main


def trigger_job():
    print("Running Scraper and Sending Job Notifications...")
    main.run()


schedule.every(3).minutes.do(trigger_job)
# schedule.every().hour.do(trigger_job)
# schedule.every().day.at("06:24").do(trigger_job)

while 1:
    schedule.run_pending()
    time.sleep(1)
