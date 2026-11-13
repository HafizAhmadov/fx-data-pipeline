import argparse
import logging
import time
from datetime import date

import pandas as pd

from load import get_last_loaded_date
from main import run

logger = logging.getLogger(__name__)

PAUSE_SECONDS = 1
DEFAULT_START = date(2023,1,1)

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
  
  logger.info("Starting backfilling: %d days from %s to %s!", len(dates), start_date, end_date)

  failed = []
  for i,d in enumerate(dates, start=1):
    try:
      run(d)
    except Exception as e:  # noqa: BLE001 - keep going if one day fails
      failed.append(d)
      logger.error("Failed %s: %s", d,e)

    if i % 50 == 0:
      logger.info("Progress: %d/%d days", i, len(dates))

    time.sleep(PAUSE_SECONDS)

  logger.info("Backfill done. Succeeded: %d, failed: %d",
                len(dates) - len(failed), len(failed))
  
  if failed:
        logger.warning("Failed dates: %s", failed)
  return failed
  

# generate_dates(date(2023,1,1), date.today())

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Load CBAR exchange rates into DuckDB.")
  parser.add_argument("--start", type=date.fromisoformat, help="Start date, YYYY-MM-DD")
  parser.add_argument("--end", type=date.fromisoformat, help="End date, YYYY-MM-DD")
  args = parser.parse_args()

  end_date = args.end or date.today()

  if args.start:
      start_date = args.start
      logger.info("Manual mode: %s to %s", start_date, end_date)
  else:
      last = get_last_loaded_date()
      start_date = last or DEFAULT_START
      logger.info("Incremental mode: last loaded %s, loading %s to %s", last, start_date, end_date)

  backfill(start_date, end_date)

