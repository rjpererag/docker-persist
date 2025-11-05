FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs

ENV PYTHONPATH=/app

RUN mkdir -p /app/data

ENV DATA_DIR=/app/data

ENV TIMER=3,4
ENV ROOT_DIR=results3
ENV SIZE=5
ENV FORMAT=CSV

CMD ["python", "-m", "src.api.entrypoint"]
