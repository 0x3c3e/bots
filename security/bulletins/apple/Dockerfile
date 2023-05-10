FROM arm64v8/python:3.10.11-slim-buster

WORKDIR /app
COPY main.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/opt/main.py"]
