FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 443/tcp

CMD ["python", "main.py"]
