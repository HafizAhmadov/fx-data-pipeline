from datetime import date 
import logging
import time
import pandas as pd

from main import run

logger = logging.getLogger(__name__)

PAUSE_SECONDS = 1

def generate_dates(start_date, end_date):
  if start_date > end_date : 
    raise ValueError(f"Your start date {start_date} is greater than {end_date} !")
  elif end_date > date.today():
    raise ValueError(f"Your end date {end_date} is greater than {date.today()}. Future dates only give you latest workday's results!")

  weekdays = pd.bdate_range(start=start_date, end=end_date)
  
  return [d.strftime("%d.%m.%Y") for d in weekdays]


def backfill(start_date, end_date):
  dates = generate_dates(start_date, end_date)

  if not dates:
    logger.info("No dates between %s and %s", start_date, end_date)
    return []
  
  logging.info("Starting backfilling: %d days from %s to %s!", len(dates), start_date, end_date)

  failed = []
  for i,d in enumerate(dates, start=1):
    try:
      run(d)
    except Exception as e:
      failed.append(d)
      logging.error("Failed %s: %s", d,e)
  
  if i % 50 == 0:
    logging.info("Progress: %d/%d days", i, len(dates))

  time.sleep(PAUSE_SECONDS)

  logger.info("Backfill done. Succeeded: %d, failed: %d",
                len(dates) - len(failed), len(failed))
  
  if failed:
        logger.warning("Failed dates: %s", failed)
  return failed
  

generate_dates(date(2026,11,1), date.today())

if __name__ == "__main__":
  backfill(date(2026, 10, 1), date.today())
  print("Number of weekdays in this period", len(df))
  print("First 3:", df[:3])
  print("Last 3:", df[-3:])
