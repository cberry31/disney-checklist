FROM python:3.13.5-alpine3.22

WORKDIR /app
COPY requirements.txt .
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8080
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["gunicorn --workers 4 --bind 0.0.0.0:8080 --access-logfile - server:app"]
