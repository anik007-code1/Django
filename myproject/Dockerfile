FROM python3.10.12-slim-buster

WORkDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD python3 manage.py runserver


