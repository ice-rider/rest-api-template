FROM python:3.13

WORKDIR /server

COPY requirements.txt /server

RUN pip install -r requirements.txt

COPY . /server

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

