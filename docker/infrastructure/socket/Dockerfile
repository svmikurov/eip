FROM python:3.13-slim

WORKDIR /app

COPY src/eip/infrastructure/endpoints/http_server.py .

EXPOSE 8000

CMD ["python3", "http_server.py"]