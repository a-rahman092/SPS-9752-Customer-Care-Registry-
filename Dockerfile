FROM python:3.6.5-alpine
WORKDIR /flask
ADD . /flask
RUN pip install -r requirements.txt
CMD ["python","index.py"]