# The parent image we want to build from
FROM python:3.9 

COPY . /app/

# cd into the /app directory
WORKDIR /app

# Copy from source to destination. Destination is inside /app

RUN apt-get install wget \
    && pip install pandas requests psycopg2 sqlalchemy pyarrow fastparquet \
    && chmod +x ingest_data.py \
    && chmod +x script.sh

ENTRYPOINT ["./script.sh"]