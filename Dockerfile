FROM python:3.6.1
WORKDIR /app
COPY requirements.txt /app
RUN pip freeze requirements.txt
COPY . /app
CMD python app.py
EXPOSE 8080