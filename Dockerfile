FROM python:3.11

COPY ./requirements.txt /app/
COPY ./bq_sql_gen.py /app/
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bq_sql_gen.py" ]
