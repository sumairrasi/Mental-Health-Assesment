FROM python:3.12-windowsservercore-1809

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3","app.py"]