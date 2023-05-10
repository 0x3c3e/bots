FROM arm64v8/python:3.10.11-slim-buster

COPY main.py /opt/app
COPY requirements.txt /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/opt/app/main.py"]