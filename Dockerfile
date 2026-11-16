FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY dbt/ dbt/

CMD ["sh", "-c", "python src/backfill.py && cd dbt && dbt build --target ${DBT_TARGET:-dev}"]