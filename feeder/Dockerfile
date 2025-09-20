FROM python:3.11-slim
WORKDIR /feeder
COPY dev_feeder.py /feeder/dev_feeder.py
RUN pip install redis
CMD ["python", "dev_feeder.py"]
