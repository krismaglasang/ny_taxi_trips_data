# The parent image we want to build from
FROM python:3.9 

# cd into the /app directory
WORKDIR /app

RUN apt-get install wget
RUN pip install pandas psycopg2 sqlalchemy pyarrow fastparquet

# Copy from source to destination. Destination is inside /app
COPY ingest_data.py ingest_data.py

# The commands we want to execute as we run our docker image
ENTRYPOINT ["python", "ingest_data.py"]