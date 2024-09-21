FROM alpine:3.20

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3","app.py"]