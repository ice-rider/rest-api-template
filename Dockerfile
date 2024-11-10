FROM python:3.13

WORKDIR /server

COPY requirements.txt /server

RUN pip install -r requirements.txt

COPY . /server

EXPOSE 5000

CMD ["flask", "run", "--host", "localhost", "--port", "5000"]

