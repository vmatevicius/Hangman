FROM python:3.10

WORKDIR /app
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && pip uninstall itsdangerous==2.1.2 --yes && pip install itsdangerous==2.0.1
COPY . /app
CMD python run.py