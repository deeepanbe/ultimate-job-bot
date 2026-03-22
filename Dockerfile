FROM mcr.microsoft.com/playwright/python:v1.46.0

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
