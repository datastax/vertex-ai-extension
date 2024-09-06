FROM python:3.12-slim

ENV PYTHONUNBUFFERED=True
ENV PORT=8080
ENV APP_HOME=/app

WORKDIR $APP_HOME
COPY . ./
COPY entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /entrypoint.sh

EXPOSE 8080

CMD ["/entrypoint.sh"]
