from datetime import date 

import pandas as pd

def generate_dates(start_date, end_date):
  if start_date > end_date : 
    raise ValueError(f"Your start date {start_date} is greater than {end_date} !")
  elif end_date > date.today():
    raise ValueError(f"Your end date {end_date} is greater than {date.today()}. Future dates only give you latest workday's results!")

  weekdays = pd.bdate_range(start=start_date, end=end_date)
  
  return [d.strftime("%d.%m.%Y") for d in weekdays]


generate_dates(date(2026,11,1), date.today())

if __name__ == "__main__":
  df = generate_dates(date(2023,1,1), date.today())
  print("Number of weekdays in this period", len(df))
  print("First 3:", df[:3])
  print("Last 3:", df[-3:])
