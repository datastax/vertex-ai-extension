
FROM python:3.11-slim

ENV PYTHONUNBUFFERED True
ENV PORT 8080
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD exec uvicorn extension:app --host 0.0.0.0 --port $PORT --workers 1 --reload
