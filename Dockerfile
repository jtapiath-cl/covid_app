FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
WORKDIR /app/src
RUN python setup.py
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]