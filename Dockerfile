FROM python:3.11-slim

WORKDIR /code

COPY . /code

RUN apt-get update && apt-get install -y libmagic-dev

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
