FROM python:3.13.0rc2-bookworm

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3","app.py"]