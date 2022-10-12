# 
FROM python:3.8-slim-buster


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2
#
COPY ./app /code/app

WORKDIR /code/app


# 
RUN pip3 install --no-cache-dir --upgrade -r /code/app/requirements.txt



ENV PYTHONPATH "/code/app"

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
