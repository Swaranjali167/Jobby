import schedule
import time
import main


def trigger_job():
    print("Running Scraper and Sending Job Notifications...")
    main.run()


schedule.every(5).minutes.at(":00").do(trigger_job)
# schedule.every().hour.do(trigger_job)
#schedule.every().day.at("18:05").do(trigger_job)

while True:
    schedule.run_pending()
    time.sleep(1)
