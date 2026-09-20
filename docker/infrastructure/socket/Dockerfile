FROM python:3.13-slim

WORKDIR /app

COPY src/eip/infrastructure/endpoints/http_server.py .

# Force unbuffered stdout/stderr: in Docker stdout is a pipe, not a TTY,
# so Python would buffer print() and logs wouldn't show up in real time.
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "http_server.py"]